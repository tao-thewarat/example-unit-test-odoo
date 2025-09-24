from odoo.tests.common import TransactionCase, Form
from unittest.mock import patch

class TestAccountMove(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })
        self.journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        self.account = self.env['account.account'].search([], limit=1)

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
