# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Host(models.Model):
    _name = 'audit_ssh_keys.host'

    name = fields.Char(string='Host Name')
    uri = fields.Char()
    environment = fields.Char()
    description = fields.Text(string='Description')
    users_nbr = fields.Char(compute='_get_users', string='Number of Users')
    user_ids = fields.One2many('audit_ssh_keys.user', 'host_id', string='Users')

    # Compute number of contacts non opt-out for a mailing list
    def _get_users(self):
        self.env.cr.execute('''
               select
                   h.id, count(*)
               from
                   audit_ssh_keys_host h 
                   left join audit_ssh_keys_user u on (u.host_id=h.id)              
               group by
                   h.id
           ''')
        data = dict(self.env.cr.fetchall())
        for host in self:
            host.users_nbr = data.get(host.id, 0)


class User(models.Model):
    _name = 'audit_ssh_keys.user'

    name = fields.Char()
    uri = fields.Char()
    description = fields.Text(string='Description')
    host_id = fields.Many2one('audit_ssh_keys.host', string='Host')

    keys_ids = fields.Many2many('audit_ssh_keys.key', 'audit_ssh_keys_user_key_rel',
                                  'user_id', 'key_id', string='SSH keys')


class SshKey(models.Model):
    _name = 'audit_ssh_keys.key'

    label = fields.Char(string="Label")
    key_type = fields.Char(string='Type')
    key_hash = fields.Text()
    uri = fields.Char()
    description = fields.Text(string='Description')
    user_ids = fields.Many2many('audit_ssh_keys.user', 'audit_ssh_keys_user_key_rel',
                                'user_id', 'key_id', string='Users')
