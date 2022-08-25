from odoo import api, fields, models, _, tools
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
from dateutil.relativedelta import relativedelta
from datetime import date
import re


class CrmBod(models.Model):
    _inherit = 'crm.lead'

    insdustry = fields.Selection(string="Insdustry", selection=[('apparel', 'Apparel / ثياب'),
                                                                ('biotechnology','Biotechnology / التكنولوجيا الحيوية'),
                                                                ('chemicals',
                                                                 'Chemicals / مواد كيميائية'),
                                                                ('communications',
                                                                 'Communications '),
                                                                ('construction ', 'Construction / مقاولات '),
                                                                ('consulting', 'consulting  / استشارى '),
                                                                ('education ', 'Education / تعليم'),
                                                                (
                                                                'electronics  ', 'Electronics / إلكترونيات'),
                                                                ('energy ', 'Energy / طاقة'),
                                                                ('engineering', 'Engineering / هندسة'),
                                                                ('entertainment', 'Entertainment  / ترفيه'),
                                                                ('environmental', 'Environmental / بيئي'),
                                                                ('finance', 'Finance  / تمويل'),
                                                                ('food & beverage',
                                                                 'Food & Beverage / طعام وشراب'),
                                                                ('healthcare',
                                                                 'Healthcare / الرعاية الصحية'),
                                                                ('insurance', 'Insurance  / تأمين'),
                                                                ('machinery ', 'Machinery / الات'),
                                                                ('manufacturing', 'Manufacturing / تصنيع'),
                                                                ('media', 'Media / وسائل الإعلام'),
                                                                ('retail / بيع بالتجزئة', 'Retail / بيع بالتجزئة'),
                                                                ('shipping  ', 'Shipping  / شحن'),
                                                                ('techology/',
                                                                 'Techology / علم التكنولوجيا'),
                                                                ('telecommunication  ',
                                                                 'Telecommunication  / اتصالات'),
                                                                ('transportation ',
                                                                 'Transportation / وسائل النقل'),
                                                                ('utilities ', 'Utilities / خدمات'),
                                                                ('mining ', 'Mining / تعدين'),
                                                                ('water Supplly',
                                                                 'Water Supply / امدادات المياه'),
                                                                ('energy Supply ',
                                                                 'Energy Supply / امدادات الطاقة'),
                                                                ('agriculture', 'Agriculture / زراعة'),
                                                                ], required=False, )

    type_new = fields.Selection(string="Type", selection=[('private', 'Private'),
                                                   ('government', 'Government'),
                                                   ('individual', 'Individual'),
                                                   ('student', 'Student'),
                                                   ('consulting', 'Consulting'),
                                                   ('retail', 'Retail'), ], required=False, )

    department = fields.Selection(string="", selection=[('general management', 'General Management'),
                                                        ('marketing department', 'Marketing Department'),
                                                        ('operations department', 'Operations Department'),
                                                        ('finance department', 'Finance Department'),
                                                        ('sales department', 'Sales Department'),
                                                        ('purchase department', 'Purchase Department'),
                                                        ('tendering ', 'Tendering '),
                                                        ('project management ', 'project management '),
                                                        ('service department', 'Service Department'), ], required=False, )

    organization_english_name = fields.Text(string="Organization English Name", required=False, )
    need = fields.Text(string="Need", required=False, )
    mobile_2 = fields.Char(string="Mobile2", required=False, )
    fax = fields.Char(string="Fax", required=False, )


    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """ Extract data from lead to create a partner.

       :param name : furtur name of the partner
       :param is_company : True if the partner is a company
       :param parent_id : id of the parent partner (False if no parent)

       :return: dictionary of values to give at res_partner.create()
       """
        email_split = tools.email_split(self.email_from)
        res = {
            'name': partner_name,
            'user_id': self.env.context.get('default_user_id') or self.user_id.id,
            'comment': self.description,
            'team_id': self.team_id.id,
            'parent_id': parent_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': email_split[0] if email_split else False,
            'title': self.title.id,
            'function': self.function,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id.id,
            'state_id': self.state_id.id,
            'website': self.website,
            'is_company': is_company,
            'type': 'contact',
            'insdustry_ee': self.insdustry,
            'type_two': self.type_new,
            'department_new': self.department,
            'organization_english_name_two': self.organization_english_name,
            'need_new': self.need,
            'new_mobile': self.mobile_2,
            'new_fax': self.fax,
        }
        if self.lang_id:
            res['lang'] = self.lang_id.code
        return res

class ContactBod(models.Model):
    _inherit = 'res.partner'
    insdustry_ee = fields.Selection(string="Insdustry", selection=[('apparel', 'Apparel / ثياب'),
                                                                ('biotechnology','Biotechnology / التكنولوجيا الحيوية'),
                                                                ('chemicals',
                                                                 'Chemicals / مواد كيميائية'),
                                                                ('communications',
                                                                 'Communications '),
                                                                ('construction ', 'Construction / مقاولات '),
                                                                ('consulting', 'consulting  / استشارى '),
                                                                ('education ', 'Education / تعليم'),
                                                                (
                                                                'electronics  ', 'Electronics / إلكترونيات'),
                                                                ('energy ', 'Energy / طاقة'),
                                                                ('engineering', 'Engineering / هندسة'),
                                                                ('entertainment', 'Entertainment  / ترفيه'),
                                                                ('environmental', 'Environmental / بيئي'),
                                                                ('finance', 'Finance  / تمويل'),
                                                                ('food & beverage',
                                                                 'Food & Beverage / طعام وشراب'),
                                                                ('healthcare',
                                                                 'Healthcare / الرعاية الصحية'),
                                                                ('insurance', 'Insurance  / تأمين'),
                                                                ('machinery ', 'Machinery / الات'),
                                                                ('manufacturing', 'Manufacturing / تصنيع'),
                                                                ('media', 'Media / وسائل الإعلام'),
                                                                ('retail / بيع بالتجزئة', 'Retail / بيع بالتجزئة'),
                                                                ('shipping  ', 'Shipping  / شحن'),
                                                                ('techology/',
                                                                 'Techology / علم التكنولوجيا'),
                                                                ('telecommunication  ',
                                                                 'Telecommunication  / اتصالات'),
                                                                ('transportation ',
                                                                 'Transportation / وسائل النقل'),
                                                                ('utilities ', 'Utilities / خدمات'),
                                                                ('mining ', 'Mining / تعدين'),
                                                                ('water Supplly',
                                                                 'Water Supply / امدادات المياه'),
                                                                ('energy Supply ',
                                                                 'Energy Supply / امدادات الطاقة'),
                                                                ('agriculture', 'Agriculture / زراعة'),
                                                                ], required=False, )

    type_two = fields.Selection(string="Type", selection=[('private', 'Private'),
                                                   ('government', 'Government'),
                                                   ('individual', 'Individual'),
                                                   ('student', 'Student'),
                                                   ('consulting', 'Consulting'),
                                                   ('retail', 'Retail'), ], required=False, )


    department_new = fields.Selection(string="Department", selection=[('general management', 'General Management'),
                                                        ('marketing department', 'Marketing Department'),
                                                        ('operations department', 'Operations Department'),
                                                        ('finance department', 'Finance Department'),
                                                        ('sales department', 'Sales Department'),
                                                        ('purchase department', 'Purchase Department'),
                                                        ('tendering ', 'Tendering '),
                                                        ('project management ', 'project management '),
                                                        ('service department', 'Service Department'), ], required=False, )

    organization_english_name_two = fields.Text(string="Organization English Name", required=False, )
    need_new = fields.Text(string="Need", required=False, )
    new_mobile = fields.Char(string="Mobile2", required=False, )
    new_fax = fields.Char(string="Fax", required=False, )

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

