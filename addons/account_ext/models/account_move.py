from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    reason = fields.Char(string="Reason")
