from odoo import models, fields, api
from . import rdf_manager
from . import query
from . import person_dal

_rdf_store = rdf_manager.RdfStore()
_query = query.Person
_dal = person_dal.PersonDal()


class Person(models.Model):
    _name = 'audit_ssh_keys.person'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    title = fields.Char(string='Title')

    workstation_ids = fields.One2many('audit_ssh_keys.workstation', 'person_id', string='Workstations')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return _rdf_store.execute(_query.get_person_workstations % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return _rdf_store.execute(_query.get_persons % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return self.search(None, offset, limit, order)

    @api.model
    def create(self, data):
        # for key, val in data.items():
        #     if hasattr(self, key):
        #         setattr(self, key, val)
        record = self.new(data)
        _id = _dal.insert(record)
        record._ids = (_id,)
        return record

    @api.multi
    def write(self, data):
        _dal.update(self.id, data)
        return True

    @api.multi
    def unlink(self):
        _dal.delete(self.id)
