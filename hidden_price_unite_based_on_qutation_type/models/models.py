from odoo import api, fields, models

class qoute_type(models.Model):
    _inherit = 'sale.order'

    quote_type = fields.Selection(string="Tender Qutation", selection=[('offer', 'Offer'), ('tender', 'Tender')])


class NewModuleunit(models.Model):
    _inherit = 'sale.order.line'

    quote_type_line = fields.Selection(string="Tender Qutation", selection=[('offer', 'Offer'), ('tender', 'Tender')] , related='order_id.quote_type')
    new_field_id = fields.Many2one(comodel_name="sale.order", string="", required=False, )
