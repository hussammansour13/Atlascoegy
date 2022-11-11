# -*- coding: utf-8 -*-
# from odoo import http


# class CrmActivity(http.Controller):
#     @http.route('/crm_activity/crm_activity', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_activity/crm_activity/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_activity.listing', {
#             'root': '/crm_activity/crm_activity',
#             'objects': http.request.env['crm_activity.crm_activity'].search([]),
#         })

#     @http.route('/crm_activity/crm_activity/objects/<model("crm_activity.crm_activity"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_activity.object', {
#             'object': obj
#         })
