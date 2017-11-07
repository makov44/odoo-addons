from odoo import models, fields, api
from . import rdf_manager
from . import query

RDF_STORE = rdf_manager.RdfStore()
Query = query.User()


class User(models.Model):
    _name = 'audit_ssh_keys.user'

    name = fields.Char()
    description = fields.Text(string='Description')
    host_id = fields.Many2one('audit_ssh_keys.host', string='Host')
    keys_ids = fields.One2many('audit_ssh_keys.key', 'user_id', string='SSH keys')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return RDF_STORE.execute(Query.get_user_keys % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.get_users % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return self.search(None, offset, limit, order)

    @api.multi
    def view(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'audit_ssh_keys.user',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'flags': {'form': {'action_buttons': True}}
        }
