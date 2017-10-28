# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import rdf_manager

RDF_STORE = rdf_manager.RdfStore()
Query = rdf_manager.Query

class Host(models.Model):
    _name = 'audit_ssh_keys.host'

    host = fields.Char(string='Host Name')
    uri = fields.Char()
    environment = fields.Char()
    description = fields.Text(string='Description')
    users_nbr = fields.Char()
    users_ids = fields.One2many('audit_ssh_keys.user', 'host_id', string='Users')
    _rdf_store = None

    @api.multi
    def write(self, vals):
        pass

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        result = super().read(fields=None, load='_classic_read')
        id = self.ids[0]
        return RDF_STORE.execute(Query.host % (id))

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=True):
    #     return [item["id"] for item in RDF_STORE.execute(RDF_STORE.host_count_query % (limit, offset))]

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        Performs a ``search()`` followed by a ``read()``.

        :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        :return: List of dictionaries containing the asked fields.
        :rtype: List of dictionaries.

        """

        return RDF_STORE.execute(Query.hosts % (limit, offset))


class User(models.Model):
    _name = 'audit_ssh_keys.user'

    name = fields.Char()
    uri = fields.Char()
    description = fields.Text(string='Description')
    host_id = fields.Many2one('audit_ssh_keys.host', string='Host')
    keys_nbr = fields.Char()
    keys_ids = fields.One2many('audit_ssh_keys.key', 'user_id', string='SSH keys')




class SshKey(models.Model):
    _name = 'audit_ssh_keys.key'

    label = fields.Char(string="Label")
    key_type = fields.Char(string='Type')
    key_hash = fields.Text()
    uri = fields.Char()
    description = fields.Text(string='Description')
    user_id = fields.Many2one('audit_ssh_keys.user', string="User")
