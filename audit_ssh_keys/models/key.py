# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import rdf_manager
from . import query

RDF_STORE = rdf_manager.RdfStore()
Query = query.Key()


class SshKey(models.Model):
    _name = 'audit_ssh_keys.key'

    name = fields.Char(string="Label")
    key_type = fields.Char(string='Type')
    key_hash = fields.Text()
    description = fields.Text(string='Description')
    user_id = fields.Many2one('audit_ssh_keys.user', string="User")

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return RDF_STORE.execute(Query.get_key % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.get_keys % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return RDF_STORE.execute(Query.get_keys % (limit, offset))

    @api.multi
    def view(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'audit_ssh_keys.key',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'flags': {'form': {'action_buttons': True}}
        }
