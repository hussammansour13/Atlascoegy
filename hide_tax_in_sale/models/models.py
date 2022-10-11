from odoo import api, fields, models, _, tools
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
from dateutil.relativedelta import relativedelta
from datetime import date


class sale(models.Model):
    _inherit = 'sale.order'