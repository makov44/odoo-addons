from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Alias(models.Model):
    _name = 'ringmail_reg.alias'

    name = fields.Char(string='Email Address', required=True)
    state = fields.Selection([
        ('draft', 'Not Confirmed'),
        ('sent', 'Confirmation Sent'),
        ('done', 'Confirmed'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')

    @api.multi
    def send_confirmation_email(self):
        user = self.env.user
        template = self.env.ref('ringmail_reg.verification_email', raise_if_not_found=False)
        assert template._name == 'mail.template'
        for alias in self:
            template.with_context(lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True,
                                                            email_values={'email_to': alias.name})
            alias.state = 'sent'
            _logger.info("Verification email sent for user <%s> to <%s>", user.login, alias.name)
