from odoo import models, fields, api
from . import rdf_manager
from . import query

RDF_STORE = rdf_manager.RdfStore()
Query = query.Workstation()


class Workstation(models.Model):
    _name = 'audit_ssh_keys.workstation'

    name = fields.Char()
    description = fields.Text(string='Description')
    key_name = fields.Char(string='Ssh Key Label')
    key = fields.Text(string="Ssh Public Key")
    person_id = fields.Many2one("audit_ssh_keys.person", string="Person")

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return RDF_STORE.execute(Query.get_workstation % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.get_workstations % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return self.search(None, offset, limit, order)

    @api.model
    def create(self, data):
        res = super(Workstation, self).create(data)
        return res

    @api.multi
    def write(self, data):
        res = super(Workstation, self).write(data)
        return res

    @api.multi
    def unlink(self):
        res = super(Workstation, self).unlink()
        return res
