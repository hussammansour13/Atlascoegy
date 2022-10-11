# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models



class saleorderone(models.Model):
    _inherit = 'sale.order'



fields_view_get_extra = saleorderone.fields_view_get

def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    result = fields_view_get_extra(self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

    if self.env.user.has_group('Hide_Main_Buttons.hide_create_button_sale'):
        temp = etree.fromstring(result['arch'])
        temp.set('create', '0')
        result['arch'] = etree.tostring(temp)

    if self.env.user.has_group('Hide_Main_Buttons.hide_edit_button_sale'):
        temp = etree.fromstring(result['arch'])
        temp.set('edit', '0')
        result['arch'] = etree.tostring(temp)
    return result

    # return result

saleorderone.fields_view_get = fields_view_get

