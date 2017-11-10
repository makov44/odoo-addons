from odoo import models, fields, api
from . import person_dal
from . import workstation
from . import workstation_dal

_dal = person_dal.PersonDal()
_workstation_dal = workstation_dal.WorkstationDal()


class Person(models.Model):
    _name = 'audit_ssh_keys.person'

    name = fields.Char(string="Name")
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    title = fields.Char(string='Title')

    # workstation_ids = fields.One2many('audit_ssh_keys.workstation', 'person_id', string='Workstations')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        return _dal.select_by_ids(self.ids)

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return _dal.select_all(offset, limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return self.search(None, offset, limit, order)

    @api.model
    def create(self, data):
        record = self.new(data)
        _id = _dal.insert(record)
        record._ids = (_id,)
        return record

    @api.multi
    def write(self, data):
        # workstation_ids = []
        # for key, value in data.items():
        #     if isinstance(value, list):
        #         for item in value:
        #             for val in item:
        #                 if isinstance(val, dict):
        #                     val['person_id'] = self.id
        #                     _id = _workstation_dal.insert(val)
        #                     workstation_ids.append(_id)
        # data["workstation_ids"] = workstation_ids
        _dal.update(self.id, data)
        return True

    @api.multi
    def unlink(self):
        _dal.delete(self.ids)
