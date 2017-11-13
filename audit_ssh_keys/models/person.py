from odoo import models, fields, api
from odoo.exceptions import ValidationError
from . import person_dal

_dal = person_dal.PersonDal()


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
        self._check_name(data['name'])
        _id = _dal.insert(data)
        record = self.new(data)
        record._ids = (_id,)
        return record

    @api.multi
    def write(self, data):
        _dal.update(self.id, data)
        return True

    @api.multi
    def unlink(self):
        _dal.delete(self.ids)

    def _check_name(self, name):
        if ' ' in name:
            raise ValidationError('Error: \'Name\' can not contain spaces!')
        return True
