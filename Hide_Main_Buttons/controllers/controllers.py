# -*- coding: utf-8 -*-
# from odoo import http


# class MakanTracking(http.Controller):
#     @http.route('/makan_tracking/makan_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/makan_tracking/makan_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('makan_tracking.listing', {
#             'root': '/makan_tracking/makan_tracking',
#             'objects': http.request.env['makan_tracking.makan_tracking'].search([]),
#         })

#     @http.route('/makan_tracking/makan_tracking/objects/<model("makan_tracking.makan_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('makan_tracking.object', {
#             'object': obj
#         })
