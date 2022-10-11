# -*- coding: utf-8 -*-
# from odoo import http


# class ReadonlyBasedGroup(http.Controller):
#     @http.route('/readonly_based_group/readonly_based_group', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/readonly_based_group/readonly_based_group/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('readonly_based_group.listing', {
#             'root': '/readonly_based_group/readonly_based_group',
#             'objects': http.request.env['readonly_based_group.readonly_based_group'].search([]),
#         })

#     @http.route('/readonly_based_group/readonly_based_group/objects/<model("readonly_based_group.readonly_based_group"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('readonly_based_group.object', {
#             'object': obj
#         })
