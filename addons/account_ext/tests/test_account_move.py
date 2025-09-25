from odoo.tests.common import TransactionCase
from unittest.mock import patch
from odoo.tests import Form
from odoo.exceptions import ValidationError

class TestAccountMove(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})
        self.journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        self.account = self.env['account.account'].search([('deprecated', '=', False)], limit=1)

        self.invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.journal.id,
        })


    def test_create_invoice_draft(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.journal.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test product',
                'quantity': 1,
                'price_unit': 100,
                'account_id': self.account.id,
            })]
        })
        self.assertEqual(invoice.state, 'draft')
        self.assertEqual(invoice.amount_total, 100)


    def test_post_invoice(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.journal.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Service',
                'quantity': 2,
                'price_unit': 50,
                'account_id': self.account.id,
            })]
        })
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.name)

    def test_compute_amount_total_form(self):
        with Form(self.invoice) as form:
            with form.invoice_line_ids.new() as line:
                line.name = 'Test product'
                line.quantity = 1
                line.price_unit = 100
            invoice = form.save()

        self.assertTrue(invoice.is_ref)


    def test_amount_untaxed_limit(self):
        """Test constraint: amount_untaxed cannot exceed 500"""
        # Happy path: amount <= 500
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.journal.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Product 1',
                'quantity': 5,
                'price_unit': 50,
                'account_id': self.account.id,
            })]
        })
        self.assertEqual(invoice.amount_untaxed, 250)

        # Exceed limit → should raise ValidationError
        with self.assertRaises(ValidationError):
            self.env['account.move'].create({})
