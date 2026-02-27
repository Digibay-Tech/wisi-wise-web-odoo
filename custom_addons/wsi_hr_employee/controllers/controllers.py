# from odoo import http


# class WsiHrEmployee(http.Controller):
#     @http.route('/wsi_hr_employee/wsi_hr_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wsi_hr_employee/wsi_hr_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wsi_hr_employee.listing', {
#             'root': '/wsi_hr_employee/wsi_hr_employee',
#             'objects': http.request.env['wsi_hr_employee.wsi_hr_employee'].search([]),
#         })

#     @http.route('/wsi_hr_employee/wsi_hr_employee/objects/<model("wsi_hr_employee.wsi_hr_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wsi_hr_employee.object', {
#             'object': obj
#         })

