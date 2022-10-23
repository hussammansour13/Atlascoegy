from odoo import api, fields, models


class NewModulecrm(models.Model):
    _inherit = 'crm.lead'

    expected_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency', tracking=True,related='new_field_id.amount_total')
    new_field_id = fields.Many2one(comodel_name="sale.order", string="Sale Order Num", required=False, )
