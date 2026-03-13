# from odoo import http


# class CustomHrEmployee(http.Controller):
#     @http.route('/custom_hr_employee/custom_hr_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_hr_employee/custom_hr_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_hr_employee.listing', {
#             'root': '/custom_hr_employee/custom_hr_employee',
#             'objects': http.request.env['custom_hr_employee.custom_hr_employee'].search([]),
#         })

#     @http.route('/custom_hr_employee/custom_hr_employee/objects/<model("custom_hr_employee.custom_hr_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_hr_employee.object', {
#             'object': obj
#         })

