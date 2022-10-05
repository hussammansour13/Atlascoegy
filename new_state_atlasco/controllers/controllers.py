# -*- coding: utf-8 -*-
# from odoo import http


# class NewStateAtlasco(http.Controller):
#     @http.route('/new__state__atlasco/new__state__atlasco', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new__state__atlasco/new__state__atlasco/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('new__state__atlasco.listing', {
#             'root': '/new__state__atlasco/new__state__atlasco',
#             'objects': http.request.env['new__state__atlasco.new__state__atlasco'].search([]),
#         })

#     @http.route('/new__state__atlasco/new__state__atlasco/objects/<model("new__state__atlasco.new__state__atlasco"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new__state__atlasco.object', {
#             'object': obj
#         })
