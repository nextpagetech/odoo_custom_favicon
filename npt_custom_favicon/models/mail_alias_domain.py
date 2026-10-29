from odoo import fields, models

class AliasDomain(models.Model):
    _inherit = 'mail.alias.domain'

    name = fields.Char(
        'Name', required=True,
        help="Email domain e.g. 'example.com' in 'company@example.com'")
