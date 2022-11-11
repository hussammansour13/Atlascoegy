# -*- coding: utf-8 -*-
# from odoo import http


# class ExpectedRevenue(http.Controller):
#     @http.route('/expected__revenue/expected__revenue', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expected__revenue/expected__revenue/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('expected__revenue.listing', {
#             'root': '/expected__revenue/expected__revenue',
#             'objects': http.request.env['expected__revenue.expected__revenue'].search([]),
#         })

#     @http.route('/expected__revenue/expected__revenue/objects/<model("expected__revenue.expected__revenue"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expected__revenue.object', {
#             'object': obj
#         })
