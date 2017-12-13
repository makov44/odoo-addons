# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import werkzeug

import odoo
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo.http import request
from twilio.rest import Client
import random

_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):
    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(AuthSignupHome, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))
        return response

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                qcontext["error"] = _("Another user is already registered using this email address.")
                return request.render('auth_signup.signup', qcontext)
            try:
                request.session['login'] = request.params["login"]
                request.session['password'] = request.params["password"]
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user and template:
                        template.sudo().with_context(
                            lang=user.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user.login}),
                            password=request.params.get('password')
                        ).send_mail(user.id, force_send=True)

                query = {"login": qcontext.get('login')}
                return werkzeug.utils.redirect("/web/signup/email_sent?%s" % werkzeug.urls.url_encode(query), 303)
            except UserError as e:
                qcontext['error'] = str(e)
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        return request.render('auth_signup.signup', qcontext)

    @http.route('/web/signup/email_sent', type='http', auth='public', website=True, sitemap=False)
    def signup_email_sent(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                template = request.env.ref('auth_signup.verification_email', raise_if_not_found=False)

                assert template._name == 'mail.template'

                user = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                if not user.email:
                    raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
                template.sudo().with_context(lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True)
                _logger.info("Verification email sent for user <%s> to <%s>", user.login, user.email)

            except UserError as e:
                qcontext['error'] = "Failed to send confirmation email"
                _logger.error(e)

        qcontext["message"] = "Verification email sent to address \'%s\'" % qcontext.get('login')
        return request.render('auth_signup.email_sent', qcontext)

    @http.route('/web/verify/email', type='http', auth='public', website=True, sitemap=False)
    def verify_email(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if not qcontext.get('token'):
            qcontext['error'] = "Email address \'%s\' was not verified yet. Check your email box." % qcontext.get('login')
            return request.render('auth_signup.verify_email', qcontext)

        if 'error' not in qcontext and request.httprequest.method == 'GET':
            qcontext["message"] = "Your email address has been successfully verified.\
                        Next step is to verify your phone number. Click a ‘send’ button to send verification code to \
                        your phone: %s" % qcontext['phone']
            partners = request.env["res.partner"].sudo().search([("signup_token", "=", qcontext.get('token'))])
            for partner in partners:
                partner.sudo().write({"signup_email_verified": True})
        elif 'error' not in qcontext and request.httprequest.method == 'POST':
            try:

                message = self._send_verification_code(qcontext)
                _logger.info(str(message))
                query = {
                    "db": qcontext["db"],
                    "token": qcontext['token']
                }
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                redirect_url = werkzeug.urls.url_join(base_url,
                                                      '/web/verify/phone?%s' % werkzeug.urls.url_encode(query))
                return request.redirect(redirect_url)
            except Exception as e:
                _logger.error(e)
                qcontext['error'] = "Failed to send verification code."

        return request.render('auth_signup.verify_email', qcontext)

    @http.route('/web/not_verified/email', type='http', auth='public', website=True, sitemap=False)
    def not_verified_email(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if request.httprequest.method == 'GET':
            qcontext['error'] = "Email address \'%s\' was not verified yet. Check your email box." % qcontext.get(
                'login')
        elif 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                template = request.env.ref('auth_signup.verification_email', raise_if_not_found=False)
                assert template._name == 'mail.template'
                user = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                partner = user.partner_id
                if partner:
                    partner.write({'signup_type': "verify"})
                if not user.email:
                    raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
                template.sudo().with_context(lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True)
                qcontext["message"] = "Verification email sent to address \'%s\'" % qcontext.get('login')
                _logger.info("Verification email sent for user <%s> to <%s>", user.login, user.email)

            except UserError as e:
                qcontext['error'] = "Failed to send confirmation email"
                _logger.error(e)

        return request.render('auth_signup.email_sent', qcontext)

    @http.route('/web/verify/phone', type='http', auth='public', website=True, sitemap=False)
    def verify_phone(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if not qcontext.get('token'):
            raise werkzeug.exception.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'GET':
            qcontext["message"] = "Verification code has been sent to your phone: %s" % qcontext["phone"]
        elif 'error' not in qcontext and request.httprequest.method == 'POST':
            if self._verify_code(qcontext):
                partners = request.env["res.partner"].sudo().search([("signup_token", "=", qcontext.get('token'))])
                for partner in partners:
                    partner.sudo().write({"signup_phone_verified": True})
                uid = request.session.authenticate(request.session.db, request.session['login'],
                                                   request.session['password'])
                if uid is not False:
                    request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect=None))
            else:
                qcontext['error'] = "Failed to verify your phone number. Try again."
        return request.render('auth_signup.verify_phone', qcontext)

    @http.route('/web/not_verified/phone', type='http', auth='public', website=True, sitemap=False)
    def not_verified_phone(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if not qcontext.get('token'):
            raise werkzeug.exception.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                partners = request.env["res.partner"].sudo().search([("signup_token", "=", qcontext.get('token'))])
                for partner in partners:
                    qcontext["phone"] = partner.phone
                    qcontext["token"] = partner.signup_token
                    message = self._send_verification_code(qcontext)
                    _logger.info(str(message))
                    base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    query = {"token": qcontext.get('token')}
                    redirect_url = werkzeug.urls.url_join(base_url,
                                                          '/web/verify/phone?%s' % werkzeug.urls.url_encode(query))
                    return request.redirect(redirect_url)
            except Exception as e:
                _logger.error(e)
                qcontext['error'] = "Failed to send verification code."
                _logger.info(str(message))
        return request.render('auth_signup.phone_not_verified', qcontext)

    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not odoo.tools.config['list_db']:
            qcontext['disable_database_manager'] = True

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return super(AuthSignupHome, self).web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    request.env['res.users'].sudo().reset_password(login)
                    qcontext['message'] = _("An email has been sent with credentials to reset your password")
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def get_auth_signup_config(self):
        """retrieve the module config (which features are enabled) for the login page"""

        get_param = request.env['ir.config_parameter'].sudo().get_param
        return {
            'signup_enabled': get_param('auth_signup.allow_uninvited') == 'True',
            'reset_password_enabled': get_param('auth_signup.reset_password') == 'True',
        }

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering context for signup and reset password """
        qcontext = request.params.copy()
        qcontext.update(self.get_auth_signup_config())
        if not qcontext.get('token') and request.session.get('auth_signup_token'):
            qcontext['token'] = request.session.get('auth_signup_token')
        if qcontext.get('token'):
            try:
                # retrieve the user info (name, login or email) corresponding to a signup token
                token_infos = request.env['res.partner'].sudo().signup_retrieve_info(qcontext.get('token'))
                for k, v in token_infos.items():
                    qcontext.setdefault(k, v)
            except UserError as e:
                qcontext['invalid_token'] = True
                qcontext['error'] = str(e.name)
            except Exception as e:
                qcontext['invalid_token'] = True
                qcontext['error'] = _("Invalid signup token")
                _logger.error(e)

        return qcontext

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'first_name', 'last_name', 'phone')}
        if not values['name']:
            values['name'] = values['first_name'] + ' ' + values['last_name']
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
        if token:
            uid = request.session.authenticate(db, login, password)
            if not uid:
                raise SignupError(_('Authentication Failed.'))

    def _send_verification_code(self, qcontext):
        phone = qcontext.get("phone")
        token = qcontext.get("token")
        config = request.env['ir.config_parameter'].sudo().get_param
        account_sid = config('auth_signup.account_sid')
        auth_token = config('auth_signup.auth_token')
        client = Client(account_sid, auth_token)
        code = random.SystemRandom().randint(1000, 9999)

        partners = request.env['res.partner'].sudo().search([('signup_token', '=', token)], limit=1)
        for partner in partners:
            partner.write({'signup_code': code})

        return client.messages.create(
            to=phone,
            from_="+14243260287",
            body="RingMail Code: " + str(code))

    def _verify_code(self, qcontext):
        code = qcontext.get('signup_code')
        token = qcontext.get("token")
        partners = request.env['res.partner'].sudo().search([('signup_token', '=', token)], limit=1)
        for partner in partners:
            if partner.signup_code == code:
                return True

        return False
