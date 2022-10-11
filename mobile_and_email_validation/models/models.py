from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class contactsemailandphone(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')



    _sql_constraints = [
        ('mobile_id', 'unique (mobile)', 'The mobile must be unique!')
    ]

    @api.constrains('mobile')
    def mobile_z_method_res(self):
        for rec in self:
            if rec.mobile and re.match("^01[0125][0-9]{8}$", rec.mobile) == None:
                raise ValidationError('Mobile Must Be Valid & 11 Number')