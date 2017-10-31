# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import rdf_manager

RDF_STORE = rdf_manager.RdfStore()
Query = rdf_manager.Query

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
        return RDF_STORE.execute(Query.host % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.hosts % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return RDF_STORE.execute(Query.hosts % (limit, offset))


class User(models.Model):
    _name = 'audit_ssh_keys.user'

    name = fields.Char()
    description = fields.Text(string='Description')
    host_id = fields.Many2one('audit_ssh_keys.host', string='Host')
    keys_ids = fields.One2many('audit_ssh_keys.key', 'user_id', string='SSH keys')

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return RDF_STORE.execute(Query.user % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.users % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return RDF_STORE.execute(Query.users % (limit, offset))

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


class SshKey(models.Model):
    _name = 'audit_ssh_keys.key'

    name = fields.Char(string="Label")
    key_type = fields.Char(string='Type')
    key_hash = fields.Text()
    description = fields.Text(string='Description')
    user_id = fields.Many2one('audit_ssh_keys.user', string="User")

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        str_ids = '(' + ''.join([str(item) + ',' for item in self.ids]) + ')'
        return RDF_STORE.execute(Query.key % (str.rstrip(str_ids, ',)') + ')'))

    @api.model
    def search(self, args, offset=0, limit=10000, order=None, count=False):
        return RDF_STORE.execute(Query.keys % (limit, offset))

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10000, order=None):
        return RDF_STORE.execute(Query.keys % (limit, offset))

    @api.multi
    def view(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'audit_ssh_keys.key',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'flags': {'form': {'action_buttons': True}}
        }
