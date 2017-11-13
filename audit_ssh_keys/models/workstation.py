from odoo import models, fields, api
from . import workstation_dal

_dal = workstation_dal.WorkstationDal()


class Workstation(models.Model):
    _name = 'audit_ssh_keys.workstation'

    name = fields.Char()
    key_name = fields.Char(string='Ssh Key Label')
    key = fields.Text(string="Ssh Public Key")

    # person_id = fields.Many2one("audit_ssh_keys.person", string="Person")

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        return _dal.select_by_ids(self.ids)

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        active_id = self._context['active_id']
        return _dal.select_all(active_id, offset, limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return self.search(None, offset, limit, order)

    @api.model
    def create(self, data):
        data['active_id'] = self._context['active_id']
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
