from odoo import models, fields, api
from . import rdf_manager
from . import query

RDF_STORE = rdf_manager.RdfStore()
Query = query.Host()


class Host(models.Model):
    _name = 'audit_ssh_keys.host'

    name = fields.Char(string='Host Name')
    environment = fields.Char()
    description = fields.Text(string='Description')
    users_ids = fields.One2many('audit_ssh_keys.user', 'host_id', string='Users')

    # @api.multi
    # def write(self, vals):
    #     pass

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '('+''.join([str(item)+',' for item in self.ids])+')'
        return RDF_STORE.execute(Query.get_host_users % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.get_hosts % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return RDF_STORE.execute(Query.get_hosts % (limit, offset))