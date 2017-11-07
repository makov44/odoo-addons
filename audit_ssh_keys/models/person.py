from odoo import models, fields, api
from . import rdf_manager

RDF_STORE = rdf_manager.RdfStore()


class Person(models.Model):
    _name = 'audit_ssh_keys.person'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    # workstation_ids = fields.One2many('audit_ssh_keys.workstation', 'person_id', string='Users')

    # @api.multi
    # def write(self, vals):
    #     pass

    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     str_ids = '('+''.join([str(item)+',' for item in self.ids])+')'
    #     return RDF_STORE.execute(Query.host % (str.rstrip(str_ids, ',)') + ')'))
    #
    # @api.model
    # def search(self, args, offset=0, limit=10000, order=None, count=False):
    #     return RDF_STORE.execute(Query.hosts % (limit, offset))
    #
    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
    #     return RDF_STORE.execute(Query.hosts % (limit, offset))