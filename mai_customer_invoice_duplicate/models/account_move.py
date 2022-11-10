# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning,UserError, ValidationError
    
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    copy_invoice = fields.Boolean('Copy Invoiced?')


class GenerateAccountMove(models.TransientModel):
    _name = "generate.account.move"
    _description = "Generate Account Move"

    def _default_invoice_ids(self):
        if len(self.env.user.company_ids) < 2:
            raise ValidationError(_("You don't have access to create Invoice for Another Company!"))
        invoice_ids = self.env.context.get('active_ids', [])
        invoice_ids = self.env['account.move'].browse(invoice_ids)

        if any(rec.copy_invoice for rec in invoice_ids):
            raise ValidationError(_("The invoices/bills have been duplicated satisfactory in draft state in other company!"))
        return invoice_ids.ids

    user_id = fields.Many2one('res.users', default=lambda x: x.env.user.id)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
        ], string='Status', required=True,
        default='posted')
    company_id = fields.Many2one('res.company', 'Company', required=True)
    tax_ids = fields.Many2many('account.tax', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    exchange_currency = fields.Boolean('Exchange Currency?')
    currency_id = fields.Many2one('res.currency')
    currency_rate = fields.Float('Currency Rate')
    # journal_id = fields.Many2one('account.journal', 'Journal', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True)
    # account_id = fields.Many2one('account.account', 'Account', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True)
    invoice_ids = fields.Many2many('account.move', default=_default_invoice_ids)

    @api.onchange('currency_id')
    def onchange_currency_rate(self):
        self.currency_rate = 0.0
        if self.currency_id:
            self.currency_rate = self.currency_id.rate

    def create_account(self, lines, company_id):
        for line in lines:
            self._cr.execute('SELECT id FROM account_account WHERE code = %s and company_id = %s', (line.account_id.code, company_id,))
            res = self._cr.fetchone()
            if not res:
                self._cr.execute('INSERT INTO account_account (code, name, company_id, user_type_id, reconcile) values (%s, %s,%s, %s,%s)', (line.account_id.code, line.account_id.name, company_id, line.account_id.user_type_id.id, line.account_id.reconcile))
        return True

    def generate_move(self):
        AccountMove = self.env['account.move'].with_context(default_move_type='entry')
        company_id = self.company_id.id
        currency_id = self.currency_id.id
        if any(rec.id for rec in self.invoice_ids if rec.state != self.state):
            raise ValidationError(_("You have not selected the (%s) invoices!") % (self.state.title()))
        for invoice_id in self.invoice_ids:
            currency_id =  invoice_id.currency_id.id if not self.exchange_currency else self.currency_id.id
            journal_id = self.env['account.journal'].search([
                    ('company_id', '=', company_id),
                    ('code', '=', invoice_id.journal_id.code)
                ], limit=1)
            if not journal_id:
                journal_id = invoice_id.journal_id.with_context({'company_id':self.company_id.id}).copy()
                journal_id.company_id = company_id

            move_vals = {
                'invoice_date': fields.Datetime.now(),
                'ref': invoice_id.name,
                'journal_id': journal_id.id,
                'currency_id': currency_id,
                'partner_id':  invoice_id.partner_id.id,
                'invoice_line_ids': [],
                'move_type': invoice_id.move_type,
            }
            invoice_id.copy_invoice = True
            self.create_account(invoice_id.invoice_line_ids, company_id)
            account_data_dict = []
            for line in invoice_id.invoice_line_ids:
                account_id = self.env['account.account'].search([('code', '=', line.account_id.code), ('company_id', '=', company_id)], limit=1)
                price = line.price_unit
                if invoice_id.currency_id.id != currency_id:
                    price = line.price_unit * self.currency_rate
                # currency_rate = self.env['res.currency']._get_conversion_rate(invoice_id.currency_id, self.currency_id, invoice_id.company_id, invoice_id.invoice_date or fields.Date.today())
                # print("==currency_rate==", currency_rate)
                tax_ids = self.tax_ids.ids or []
                vals = {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': price,
                    'discount': line.discount,
                    'tax_ids': [(6,0, tax_ids)],
                    'account_id': account_id.id,
                }
                move_vals['invoice_line_ids'].append((0, 0, vals))

            moves = AccountMove.create(move_vals)
        return {'type': 'ir.actions.act_window_close'}
