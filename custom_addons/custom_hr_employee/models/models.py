# from odoo import models, fields, api


# class custom_hr_employee(models.Model):
#     _name = 'custom_hr_employee.custom_hr_employee'
#     _description = 'custom_hr_employee.custom_hr_employee'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

