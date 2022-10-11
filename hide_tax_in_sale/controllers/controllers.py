# -*- coding: utf-8 -*-
# from odoo import http


# class SeeHisOwnContact(http.Controller):
#     @http.route('/see_his_own_contact/see_his_own_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/see_his_own_contact/see_his_own_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('see_his_own_contact.listing', {
#             'root': '/see_his_own_contact/see_his_own_contact',
#             'objects': http.request.env['see_his_own_contact.see_his_own_contact'].search([]),
#         })

#     @http.route('/see_his_own_contact/see_his_own_contact/objects/<model("see_his_own_contact.see_his_own_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('see_his_own_contact.object', {
#             'object': obj
#         })
