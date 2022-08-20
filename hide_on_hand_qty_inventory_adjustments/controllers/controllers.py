# -*- coding: utf-8 -*-
# from odoo import http


# class HideOnHandQtyInventoryAdjustments(http.Controller):
#     @http.route('/hide_on_hand_qty__inventory__adjustments/hide_on_hand_qty__inventory__adjustments', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_on_hand_qty__inventory__adjustments/hide_on_hand_qty__inventory__adjustments/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_on_hand_qty__inventory__adjustments.listing', {
#             'root': '/hide_on_hand_qty__inventory__adjustments/hide_on_hand_qty__inventory__adjustments',
#             'objects': http.request.env['hide_on_hand_qty__inventory__adjustments.hide_on_hand_qty__inventory__adjustments'].search([]),
#         })

#     @http.route('/hide_on_hand_qty__inventory__adjustments/hide_on_hand_qty__inventory__adjustments/objects/<model("hide_on_hand_qty__inventory__adjustments.hide_on_hand_qty__inventory__adjustments"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_on_hand_qty__inventory__adjustments.object', {
#             'object': obj
#         })
