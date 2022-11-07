from odoo import api, fields, models

class newstateatlasco(models.Model):
    _inherit = 'sale.order'
    # state = fields.Selection(selection_add=[('bar', 'Bar')])
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('rejection', 'Quote Rejection'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')


    def action_rejection(self):
        for rec in self:
            rec.write({'state':'rejection'})




