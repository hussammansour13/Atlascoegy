# -*- coding: utf-8 -*-
# from odoo import http


# class SearchReadAddon(http.Controller):
#     @http.route('/search_read__addon/search_read__addon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/search_read__addon/search_read__addon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('search_read__addon.listing', {
#             'root': '/search_read__addon/search_read__addon',
#             'objects': http.request.env['search_read__addon.search_read__addon'].search([]),
#         })

#     @http.route('/search_read__addon/search_read__addon/objects/<model("search_read__addon.search_read__addon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('search_read__addon.object', {
#             'object': obj
#         })
