from odoo import api, fields, models


class serialnumstock(models.Model):
    _inherit = 'stock.move.line'

    serial_numb = fields.Char(string="Serial Num", required=False, )
