# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_pdc_payment_account = fields.Many2one('account.account', 'PDC Payment Account for Customer')
    vendor_pdc_payment_account = fields.Many2one('account.account', 'PDC Payment Account for Vendors/Suppliers')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res['customer_pdc_payment_account'] = int(
            self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account', default=0))
        res['vendor_pdc_payment_account'] = int(
            self.env['ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account', default=0))

        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('customer_pdc_payment_account',
                                                         self.customer_pdc_payment_account.id)
        self.env['ir.config_parameter'].sudo().set_param('vendor_pdc_payment_account',
                                                         self.vendor_pdc_payment_account.id)

        super(ResConfigSettings, self).set_values()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    pdc_id = fields.Many2one('sr.pdc.payment', 'Post Dated Cheques')


class AccountMove(models.Model):
    _inherit = "account.move"

    pdc_id = fields.Many2one('sr.pdc.payment', 'Post Dated Cheques')

    # @api.depends(
    #     'line_ids.debit',
    #     'line_ids.credit',
    #     'line_ids.currency_id',
    #     'line_ids.amount_currency',
    #     'line_ids.amount_residual',
    #     'line_ids.amount_residual_currency',
    #     'line_ids.payment_id.state')
    # def _compute_amount(self):
    #     invoice_ids = [move.id for move in self if move.id and move.is_invoice(include_receipts=True)]
    #     self.env['account.payment'].flush(['state'])
    #     if invoice_ids:
    #         self._cr.execute(
    #             '''
    #                 SELECT move.id
    #                 FROM account_move move
    #                 JOIN account_move_line line ON line.move_id = move.id
    #                 JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
    #                 JOIN account_move_line rec_line ON
    #                     (rec_line.id = part.credit_move_id AND line.id = part.debit_move_id)
    #                     OR
    #                     (rec_line.id = part.debit_move_id AND line.id = part.credit_move_id)
    #                 JOIN account_payment payment ON payment.id = rec_line.payment_id
    #                 JOIN account_journal journal ON journal.id = rec_line.journal_id
    #                 WHERE payment.state IN ('posted')
    #                 AND move.id IN %s
    #             ''', [tuple(invoice_ids)]
    #         )
    #         in_payment_set = set(res[0] for res in self._cr.fetchall())
    #     else:
    #         in_payment_set = {}
    #
    #     for move in self:
    #         total_untaxed = 0.0
    #         total_untaxed_currency = 0.0
    #         total_tax = 0.0
    #         total_tax_currency = 0.0
    #         total_residual = 0.0
    #         total_residual_currency = 0.0
    #         total = 0.0
    #         total_currency = 0.0
    #         currencies = set()
    #
    #         for line in move.line_ids:
    #             if line.currency_id:
    #                 currencies.add(line.currency_id)
    #
    #             if move.is_invoice(include_receipts=True):
    #                 # === Invoices ===
    #
    #                 if not line.exclude_from_invoice_tab:
    #                     # Untaxed amount.
    #                     total_untaxed += line.balance
    #                     total_untaxed_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.tax_line_id:
    #                     # Tax amount.
    #                     total_tax += line.balance
    #                     total_tax_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.account_id.user_type_id.type in ('receivable', 'payable'):
    #                     # Residual amount.
    #                     total_residual += line.amount_residual
    #                     total_residual_currency += line.amount_residual_currency
    #             else:
    #                 # === Miscellaneous journal entry ===
    #                 if line.debit:
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #
    #         if move.move_type == 'entry' or move.is_outbound():
    #             sign = 1
    #         else:
    #             sign = -1
    #         print("=======self._context======", self._context)
    #         if self._context.get('pdc'):
    #             total_residual = 0
    #         move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
    #         move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
    #         move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
    #         move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
    #         move.amount_untaxed_signed = -total_untaxed
    #         move.amount_tax_signed = -total_tax
    #         move.amount_total_signed = -total
    #         move.amount_residual_signed = total_residual
    #
    #         currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id
    #         is_paid = currency and currency.is_zero(move.amount_residual) or not move.amount_residual
    #
    #         # Compute 'payment_state'.
    #         if move.state == 'posted' and is_paid:
    #             if move.id in in_payment_set:
    #                 move.payment_state = 'in_payment'
    #             else:
    #                 move.payment_state = 'paid'
    #         else:
    #             move.payment_state = 'not_paid'


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def _compute_payment_amount(self, invoices, currency, journal, date):
        '''Compute the total amount for the payment wizard.

        :param invoices:    Invoices on which compute the total as an account.invoice recordset.
        :param currency:    The payment's currency as a res.currency record.
        :param journal:     The payment's journal as an account.journal record.
        :param date:        The payment's date as a datetime.date object.
        :return:            The total amount to pay the invoices.
        '''
        company = journal.company_id
        currency = currency or journal.currency_id or company.currency_id
        date = date or fields.Date.today()

        if not invoices:
            return 0.0

        self.env['account.move'].flush(['move_type', 'currency_id'])
        self.env['account.move.line'].flush(['amount_residual', 'amount_residual_currency', 'move_id', 'account_id'])
        self.env['account.account'].flush(['user_type_id'])
        self.env['account.account.type'].flush(['type'])
        self._cr.execute('''
            SELECT
                move.move_type AS type,
                move.currency_id AS currency_id,
                SUM(line.amount_residual) AS amount_residual,
                SUM(line.amount_residual_currency) AS residual_currency
            FROM account_move move
            LEFT JOIN account_move_line line ON line.move_id = move.id
            LEFT JOIN account_account account ON account.id = line.account_id
            LEFT JOIN account_account_type account_type ON account_type.id = account.user_type_id
            WHERE move.id IN %s
            AND account_type.type IN ('receivable', 'payable')
            GROUP BY move.id, move.move_type
        ''', [tuple(invoices.ids)])
        query_res = self._cr.dictfetchall()

        total = 0.0
        for res in query_res:
            move_currency = self.env['res.currency'].browse(res['currency_id'])
            if move_currency == currency and move_currency != company.currency_id:
                total += res['residual_currency']
            else:
                total += company.currency_id._convert(res['amount_residual'], currency, company, date)
        return total


class PdcPayment(models.Model):
    _name = "sr.pdc.payment"

    invoice_ids = fields.Many2many('account.move', 'account_invoice_pdc_rel', 'pdc_id', 'invoice_id', string="Invoices",
                                   copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, copy=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('register', 'Registered'), ('return', 'Returned'), ('deposit', 'Deposited'),
         ('bounce', 'Bounced'), ('done', 'Done'), ('cancel', 'Cancelled')], readonly=True, default='draft', copy=False,
        string="Status")
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True,
                                 domain=[('type', 'in', ['bank'])])
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
    due_date = fields.Date(string='Due Date', default=fields.Date.context_today, required=True, copy=False)
    communication = fields.Char(string='Memo')
    cheque_ref = fields.Char('Cheque Reference')
    agent = fields.Char('Agent')
    bank = fields.Many2one('res.bank', string="Bank")
    name = fields.Char('Name')
    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money')], string='Payment Type',
                                    required=True)
    amount_dued = fields.Float(string="", required=False,)

    @api.onchange('amount')
    def onchange_method(self):
        if self.amount !=0:
            self.amount_dued =  self.amount_dued - self.amount
    @api.model
    def create(self, vals):
        res = super(PdcPayment, self).create(vals)
        return res

    @api.onchange('journal_id')
    def _default_currency(self):
        if self.journal_id:
            journal = self.journal_id
            currency_id = journal.currency_id or journal.company_id.currency_id or self.env.user.company_id.currency_id
            self.currency_id = currency_id.id
        else:
            self.currency_id = False

    @api.model
    def default_get(self, default_fields):
        rec = super(PdcPayment, self).default_get(default_fields)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        active_model = self._context.get('active_model')

        # Check for selected invoices ids
        if not active_ids or active_model != 'account.move':
            return rec

        invoices = self.env['account.move'].browse(active_ids).filtered(
            lambda move: move.is_invoice(include_receipts=True))

        # Check all invoices are open
        if not invoices or any(invoice.state != 'posted' for invoice in invoices):
            raise UserError(_("You can only register payments for open invoices"))
        # Check if, in batch payments, there are not negative invoices and positive invoices
        dtype = invoices[0].move_type
        amount_due =0
        for inv in invoices[1:]:
            if inv.move_type != dtype:
                if ((dtype == 'in_refund' and inv.move_type == 'in_invoice') or
                        (dtype == 'in_invoice' and inv.move_type == 'in_refund')):
                    raise UserError(_(
                        "You cannot register Post dated cheques for vendor bills and supplier refunds at the same time."))
                if ((dtype == 'out_refund' and inv.move_type == 'out_invoice') or
                        (dtype == 'out_invoice' and inv.move_type == 'out_refund')):
                    raise UserError(_(
                        "You cannot register Post dated cheques for customer invoices and credit notes at the same time."))
        for inv in invoices:
            amount_due += inv.amount_residual

        amount = self.env['account.payment']._compute_payment_amount(invoices, invoices[0].currency_id,
                                                                     invoices[0].journal_id,
                                                                     rec.get('payment_date') or fields.Date.today())
        rec.update({
            'currency_id': invoices[0].currency_id.id,
            # 'amount': abs(amount),
            'payment_type': 'inbound' if amount > 0 else 'outbound',
            'partner_id': invoices[0].commercial_partner_id.id,
            'communication': invoices[0].payment_reference or invoices[0].ref or invoices[0].name,
            'invoice_ids': [(6, 0, invoices.ids)],
            'amount_dued':amount_due,
        })
        return rec

    def cancel(self):
        self.state = 'cancel'

    def register(self):
        inv = self.env['account.move'].browse(self._context.get('active_ids'))
        if inv:
            inv.amount_residual = self.amount_dued
            # if inv.amount_residual == 0 :
            #     inv.state ='posted'

        self.state = 'register'
        if self.payment_type == 'inbound':
            self.name = self.env['ir.sequence'].next_by_code('pdc.payment')
        else:
            self.name = self.env['ir.sequence'].next_by_code('pdc.payment.vendor')
        return

    def return_cheque(self):
        self.state = 'return'
        return

    def deposit(self):
        if self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account') and self.env[
            'ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'):
            inv = self.env['account.move'].browse(self._context.get('active_ids'))
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            if inv:
                inv.state = 'paid'
                custom_currency_id = inv.currency_id
                company_currency_id = inv.company_id.currency_id
                account_id = inv.account_id.id
            else:
                custom_currency_id = self.currency_id
                company_currency_id = self.env.user.company_id.currency_id
                if self.payment_type == 'inbound':
                    account_id = self.partner_id.property_account_receivable_id.id
                else:
                    account_id = self.partner_id.property_account_payable_id.id
            if self.currency_id != self.env.user.company_id.currency_id:
                balance = self.currency_id._convert(self.amount, company_currency_id, self.env.user.company_id,
                                                    self.due_date)
            else:
                balance = self.amount
            name = ''
            if self.invoice_ids:
                name += 'PDC Payment: '
                for record in self.invoice_ids:
                    if record.line_ids:
                        name += record.name + ', '
                name = name[:len(name) - 2]
            pdc_credit_account_id = False
            pdc_debit_account_id = False
            if self.payment_type == 'inbound':
                pdc_credit_account_id = account_id
                pdc_debit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account'))
            else:
                pdc_credit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'))
                pdc_debit_account_id = account_id
            if self.env.user.company_id.currency_id != self.currency_id:
                amount_currency = self.amount
            else:
                amount_currency = 0.0
            move_vals = {
                'date': self.due_date,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.journal_id.currency_id.id or self.currency_id.id,
                'partner_id': self.partner_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': name,
                        'amount_currency': amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': 0.0,
                        'credit': balance,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_credit_account_id,
                    }),
                    (0, 0, {
                        'name': name,
                        'amount_currency': -amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': balance,
                        'credit': 0.0,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_debit_account_id,
                    }),
                ],
            }
            move = AccountMove.create(move_vals)
            move.post()
        else:
            raise UserError(_("Configuration Error: Please define account for the PDC payment."))
        self.state = 'deposit'
        return True

    def done(self):
        if self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account') and self.env[
            'ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'):
            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            if self.currency_id != self.env.user.company_id.currency_id:
                balance = self.currency_id._convert(self.amount, company_currency_id, self.env.user.company_id,
                                                    self.due_date)
            else:
                balance = self.amount
            if self.payment_type == 'inbound':
                account_id = self.journal_id.id
            else:
                account_id = self.journal_id.id
            name = ''
            if self.invoice_ids:
                name += 'PDC Payment: '
                for record in self.invoice_ids:
                    if record.line_ids:
                        name += record.name + ', '
                name = name[:len(name) - 2]
            if self.payment_type == 'inbound':
                pdc_debit_account_id = account_id
                pdc_credit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account'))
            else:
                pdc_credit_account_id = account_id
                pdc_debit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'))
            if self.env.user.company_id.currency_id != self.currency_id:
                amount_currency = self.amount
            else:
                amount_currency = 0.0
            move_vals = {
                'date': self.due_date,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.journal_id.currency_id.id or self.currency_id.id,
                'partner_id': self.partner_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': name,
                        'amount_currency': amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': 0.0,
                        'credit': balance,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_credit_account_id,
                    }),
                    (0, 0, {
                        'name': name,
                        'amount_currency': -amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': balance,
                        'credit': 0.0,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_debit_account_id,
                    }),
                ],
            }
            move = AccountMove.create(move_vals)
            move.post()
            self.state = 'done'
            #             if self.invoice_ids:
            #                 (move + self.invoice_ids).line_ids \
            #                     .filtered(lambda line: not line.reconciled and (line.account_id.id == int(self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account')) or line.account_id.id == self.partner_id.property_account_receivable_id.id) )\
            #                     .reconcile()
            for record in self.invoice_ids:
                record.payment_state = 'paid'
        else:
            raise UserError(_("Configuration Error: Please define account for the PDC payment."))
        return True

    def bounce(self):
        if self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account') and self.env[
            'ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'):
            if self.payment_type == 'inbound':
                account_id = self.partner_id.property_account_receivable_id.id
            else:
                account_id = self.partner_id.property_account_payable_id.id
            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            if self.currency_id != self.env.user.company_id.currency_id:
                balance = self.currency_id._convert(self.amount, company_currency_id, self.env.user.company_id,
                                                    self.due_date)
            else:
                balance = self.amount
            name = ''
            if self.invoice_ids:
                name += 'PDC Payment: '
                for record in self.invoice_ids:
                    if record.line_ids:
                        name += record.name + ', '
                name = name[:len(name) - 2]
            if self.payment_type == 'inbound':
                pdc_debit_account_id = account_id
                pdc_credit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('customer_pdc_payment_account'))
            else:
                pdc_credit_account_id = account_id
                pdc_debit_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('vendor_pdc_payment_account'))
            if self.env.user.company_id.currency_id != self.currency_id:
                amount_currency = self.amount
            else:
                amount_currency = 0.0
            move_vals = {
                'date': self.due_date,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.journal_id.currency_id.id or self.currency_id.id,
                'partner_id': self.partner_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': name,
                        'amount_currency': amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': 0.0,
                        'credit': balance,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_credit_account_id,
                    }),
                    (0, 0, {
                        'name': name,
                        'amount_currency': -amount_currency,
                        'currency_id': self.currency_id.id if self.env.user.company_id.currency_id != self.currency_id else False,
                        'debit': balance,
                        'credit': 0.0,
                        'date_maturity': self.due_date,
                        'partner_id': self.partner_id.id,
                        'account_id': pdc_debit_account_id,
                    }),
                ],
            }
            move = AccountMove.create(move_vals)
            move.post()
            self.state = 'bounce'
            for record in self.invoice_ids:
                record.amount_residual = record.amount_total
        else:
            raise UserError(_("Configuration Error: Please define account for the PDC payment."))
        return True


class NewModule(models.Model):
    _inherit = 'account.move'


