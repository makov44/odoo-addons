from odoo import models, fields, api
from odoo.exceptions import UserError
import random
import base64
import dns.resolver
import requests


def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(20))

INSTRUCTIONS = """
<div style='font-family: "Lucida Grande", Helvetica, Verdana, Arial, sans-serif;font-size: 13px;color: #4c4c4c;'>
   <div>
      <h2>Verify domain:</h2>
   </div>
   <div>
      <p>1. Verify using a DNS record</p>
   </div>
   <div>
      <p>&nbsp; &nbsp; Create a TXT record that contains exactly this value:
     </p>
   </div>
    <div>
      <p>&nbsp; &nbsp; %s</p>
   </div>
   <div>
      <p>&nbsp; &nbsp; Additional Instructions:</p>
   </div>
   <div>
      <p>&nbsp; &nbsp;&nbsp;<a href="https://www.godaddy.com/help/manage-dns-zone-files-680" target="_blank" class="btn-link" title="">GoDaddy: Adding or Editing TXT Records
         &nbsp;</a>
      </p>
   </div>
   <div>
      <p>2. Verify using a web page</p>
   </div>
   <div>
      <p>&nbsp; &nbsp; Install this HTML page within the root ("/") directory of your web site:</p>
   </div>
</div>
"""


class Domain(models.Model):
    _name = 'ringmail_reg.domain'

    name = fields.Char(string='Domain Name', required=True)
    state = fields.Selection([
        ('draft', 'Not Confirmed'),
        ('done', 'Confirmed'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
    txt_record = fields.Char(string='TXT record', readonly=True, copy=False)
    page = fields.Binary(string="HTML page", readonly=True, copy=False)
    page_fname = fields.Char(string="File name", copy=False)
    instructions = fields.Html(readonly=True)

    @api.multi
    def confirm_domain(self):
        for domain in self:
            for txt_record in dns.resolver.query(domain.name, 'TXT'):
                if txt_record.to_text().replace('"', '') == domain.txt_record:
                    self.state = 'done'
                    return
            r = requests.get('http://' + domain.name + '/' + domain.page_fname)
            if r and r.txt:
                if r.txt == txt_record:
                    self.state = 'done'
                    return
        raise UserError("Can not confirm domain.")

    @api.model
    def create(self, vals):
        token = random_token()
        vals['txt_record'] = 'ringmail-domain-verify=' + token
        vals['page_fname'] = 'ringmail_' + token + '.html'
        vals['page'] = base64.encodebytes(str.encode(vals['txt_record']))
        vals['instructions'] = INSTRUCTIONS % vals['txt_record']
        return super(Domain, self).create(vals)
