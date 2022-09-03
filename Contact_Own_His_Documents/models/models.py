
from odoo import models, api
from odoo import fields as fs


class Searchreadcustom(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        user = self.env.user
        if not user.has_group('hr_contract.group_hr_contract_manager'):
            domain.append(('create_uid', '=', user.id))
            # domain.append(('date_order', '>=', fs.Datetime.today()))
            # domain.append(('date_order', '<=', fs.Datetime.today().replace(hour=23, minute=59, second=59)))
        return super(Searchreadcustom, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)