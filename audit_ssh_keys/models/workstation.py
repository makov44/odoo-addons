from odoo import models, fields, api
from . import rdf_manager

RDF_STORE = rdf_manager.RdfStore()


class Workstation(models.Model):
    _name = 'audit_ssh_keys.workstation'

    name = fields.Char()
    description = fields.Text(string='Description')


    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
    #     return RDF_STORE.execute(Query.user % (str.rstrip(str_ids, ',)') + ')'))
    #
    # @api.model
    # def search(self, args, offset=0, limit=10000, order=None, count=False):
    #     return RDF_STORE.execute(Query.users % (limit, offset))
    #
    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
    #     return RDF_STORE.execute(Query.users % (limit, offset))
    #
    # @api.multi
    # def view(self):
    #     return {
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'audit_ssh_keys.user',
    #         'res_id': self.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'flags': {'form': {'action_buttons': True}}
    #     }