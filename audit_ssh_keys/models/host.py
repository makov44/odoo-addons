from odoo import models, fields, api
from . import host_dal
from odoo.exceptions import ValidationError

_dal = host_dal.HostDal()


class Host(models.Model):
    _name = 'audit_ssh_keys.host'

    name = fields.Char(string='Host Name', required=True)
    uri = fields.Char(string='Host Name', required=True)
    environment = fields.Char(string="Environment")

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
        self._check_name(data["name"])
        record = self.new(data)
        _id = _dal.insert(data)
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
