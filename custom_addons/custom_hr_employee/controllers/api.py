from odoo import http
from odoo.http import request

class EmployeeAPI(http.Controller):

    # Route dibuat dengan decorator @http.route, menggunakan tipe json
    @http.route('/api/employee/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_employee(self, **kwargs):
        
        # Validasi payload wajib (name tidak boleh kosong)
        name = kwargs.get('name')
        if not name:
            return {
                "status": "error",
                "message": "Field 'name' is required",
                "data": {}
            }

        try:
            # Proses pembuatan data Karyawan
            # Menggunakan sudo() karena auth='public', namun perlu hati-hati untuk akses data di production
            new_employee = request.env['hr.employee'].sudo().create({
                'name': name,
                'employee_id': kwargs.get('employee_id', ''),
                'date_joined': kwargs.get('date_joined', False),
                'employee_status': kwargs.get('employee_status', 'internship')
            })

            # Standarisasi response
            return {
                "status": "success",
                "message": "Employee created successfully",
                "data": {
                    "employee_id": new_employee.id,
                    "name": new_employee.name
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "data": {}
            }