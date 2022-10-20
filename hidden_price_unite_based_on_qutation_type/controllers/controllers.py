# -*- coding: utf-8 -*-
# from odoo import http


# class HiddenPriceUniteBasedOnQutationType(http.Controller):
#     @http.route('/hidden_price_unite_based_on_qutation_type/hidden_price_unite_based_on_qutation_type', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hidden_price_unite_based_on_qutation_type/hidden_price_unite_based_on_qutation_type/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hidden_price_unite_based_on_qutation_type.listing', {
#             'root': '/hidden_price_unite_based_on_qutation_type/hidden_price_unite_based_on_qutation_type',
#             'objects': http.request.env['hidden_price_unite_based_on_qutation_type.hidden_price_unite_based_on_qutation_type'].search([]),
#         })

#     @http.route('/hidden_price_unite_based_on_qutation_type/hidden_price_unite_based_on_qutation_type/objects/<model("hidden_price_unite_based_on_qutation_type.hidden_price_unite_based_on_qutation_type"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hidden_price_unite_based_on_qutation_type.object', {
#             'object': obj
#         })
