# -*- coding: utf-8 -*-
from odoo import http

# class AuditSshKeys(http.Controller):
#     @http.route('/audit_ssh_keys/audit_ssh_keys/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/audit_ssh_keys/audit_ssh_keys/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('audit_ssh_keys.listing', {
#             'root': '/audit_ssh_keys/audit_ssh_keys',
#             'objects': http.request.env['audit_ssh_keys.audit_ssh_keys'].search([]),
#         })

#     @http.route('/audit_ssh_keys/audit_ssh_keys/objects/<model("audit_ssh_keys.audit_ssh_keys"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('audit_ssh_keys.object', {
#             'object': obj
#         })