from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    reason = fields.Char(string="Reason")
    is_ref = fields.Boolean(
        string='Is Invoice',
        compute='_compute_is_ref',
    )

    @api.depends('amount_untaxed')
    def _compute_is_ref(self):
        for rec in self:
            if rec.amount_untaxed >= 100:
                rec.is_ref = True
            else:
                rec.is_ref = False
                
    def _prepare_edi_vals_to_export(self):
        return {
            **super()._prepare_edi_vals_to_export(),
            'reason': 'hello world',
        }

    @api.constrains('amount_untaxed')
    def _check_amount_untaxed_limit(self):
        for move in self:
            if move.amount_untaxed > 500:
                raise ValidationError("Amount untaxed cannot exceed 500!")
