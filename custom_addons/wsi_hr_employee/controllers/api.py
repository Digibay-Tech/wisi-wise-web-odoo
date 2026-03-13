import json
from odoo import http
from odoo.http import request

class EmployeeAPI(http.Controller):

    # ==========================================
    # 1. CREATE (POST): UNTUK MEMBUAT KARYAWAN
    # ==========================================
    @http.route('/api/employee/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_employee(self, **kwargs):
        try:
            body_data = request.httprequest.data
            payload = json.loads(body_data)

            name = payload.get('name')
            email = payload.get('email')
            password = payload.get('password', 'password123')
            date_joined = payload.get('date_joined', False)

            if not name or not email:
                error_response = {"status": "error", "message": "Fields 'name' and 'email' are required", "data": {}}
                return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

            existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            
            if existing_user:
                user_record = existing_user
            else:
                user_record = request.env['res.users'].sudo().create({
                    'name': name,
                    'login': email,
                    'password': password
                })

            new_employee = request.env['hr.employee'].sudo().create({
                'name': name,
                'work_email': email,
                'date_joined': date_joined,
                'user_id': user_record.id, 
            })

            success_response = {
                "status": "success",
                "message": "User and Employee created & linked successfully",
                "data": {
                    "database_id": new_employee.id,
                    "employee_id": new_employee.employee_id,
                    "name": new_employee.name,
                    "email": email,
                    "linked_user_id": user_record.id
                }
            }
            return request.make_response(json.dumps(success_response), headers=[('Content-Type', 'application/json')])
            
        except Exception as e:
            error_response = {"status": "error", "message": str(e), "data": {}}
            return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

    # ==========================================
    # 2. READ (GET): MENGAMBIL DATA & PAGINATION
    # ==========================================
    @http.route('/api/employee/get', type='http', auth='public', methods=['GET'], csrf=False)
    def get_employee(self, **kwargs):
        try:
            search_id = kwargs.get('employee_id')
            
            # --- SKENARIO A: REQUEST 1 DATA SPESIFIK (Tanpa Array) ---
            if search_id:
                emp = request.env['hr.employee'].sudo().search([('employee_id', '=', search_id)], limit=1)
                if not emp:
                    error_response = {"status": "error", "message": "Employee not found", "data": {}}
                    return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])
                
                single_data = {
                    "database_id": emp.id,
                    "employee_id": emp.employee_id or "",
                    "name": emp.name or "",
                    "email": emp.work_email or "",
                    "date_joined": str(emp.date_joined) if emp.date_joined else "",
                    "employee_tenure": emp.employee_tenure or "",
                }
                success_response = {
                    "status": "success",
                    "message": "Employee found",
                    "data": single_data  # Object Tunggal, BUKAN Array
                }
                return request.make_response(json.dumps(success_response), headers=[('Content-Type', 'application/json')])

            # --- SKENARIO B: REQUEST SEMUA DATA DENGAN PAGINATION ---
            page = int(kwargs.get('page', 1))
            limit = int(kwargs.get('limit', 10))  # Default 10 data per halaman
            offset = (page - 1) * limit

            employees = request.env['hr.employee'].sudo().search([], limit=limit, offset=offset)
            total_count = request.env['hr.employee'].sudo().search_count([])
            
            employee_data = []
            for emp in employees:
                employee_data.append({
                    "database_id": emp.id,
                    "employee_id": emp.employee_id or "",
                    "name": emp.name or "",
                    "email": emp.work_email or "",
                })

            success_response = {
                "status": "success",
                "message": f"Successfully retrieved employees",
                "pagination": {
                    "total_data": total_count,
                    "total_pages": (total_count + limit - 1) // limit,
                    "current_page": page,
                    "limit_per_page": limit
                },
                "data": employee_data # Array (List)
            }
            return request.make_response(json.dumps(success_response), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            error_response = {"status": "error", "message": str(e), "data": {}}
            return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

    # ==========================================
    # 3. UPDATE (PUT): MENGUBAH DATA KARYAWAN
    # ==========================================
    @http.route('/api/employee/update', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_employee(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data)
            search_id = payload.get('employee_id')

            if not search_id:
                error_response = {"status": "error", "message": "Field 'employee_id' is required to update", "data": {}}
                return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

            emp = request.env['hr.employee'].sudo().search([('employee_id', '=', search_id)], limit=1)
            if not emp:
                error_response = {"status": "error", "message": "Employee not found", "data": {}}
                return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

            # Kumpulkan data apa saja yang ingin di-update
            update_vals = {}
            if 'name' in payload:
                update_vals['name'] = payload['name']
            if 'email' in payload:
                update_vals['work_email'] = payload['email']

            # Eksekusi update
            if update_vals:
                emp.sudo().write(update_vals)
                
                # Jika nama/email diupdate, update juga akun Login User-nya (opsional tapi disarankan)
                if emp.user_id and ('name' in payload or 'email' in payload):
                    user_vals = {}
                    if 'name' in payload: user_vals['name'] = payload['name']
                    if 'email' in payload: user_vals['login'] = payload['email']
                    emp.user_id.sudo().write(user_vals)

            success_response = {
                "status": "success",
                "message": "Employee updated successfully",
                "data": {"employee_id": emp.employee_id, "name": emp.name}
            }
            return request.make_response(json.dumps(success_response), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            error_response = {"status": "error", "message": str(e), "data": {}}
            return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

    # ==========================================
    # 4. DELETE (DELETE): MENGHAPUS DATA KARYAWAN
    # ==========================================
    @http.route('/api/employee/delete', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_employee(self, **kwargs):
        try:
            # Mengambil input dari body JSON atau URL Params
            if request.httprequest.data:
                payload = json.loads(request.httprequest.data)
                search_id = payload.get('employee_id')
            else:
                search_id = kwargs.get('employee_id')

            if not search_id:
                error_response = {"status": "error", "message": "Field 'employee_id' is required to delete", "data": {}}
                return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

            emp = request.env['hr.employee'].sudo().search([('employee_id', '=', search_id)], limit=1)
            if not emp:
                error_response = {"status": "error", "message": "Employee not found", "data": {}}
                return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])

            # Simpan nama untuk response, lalu hapus data (unlink)
            emp_name = emp.name
            emp.sudo().unlink()

            success_response = {
                "status": "success",
                "message": f"Employee '{emp_name}' deleted successfully",
                "data": {}
            }
            return request.make_response(json.dumps(success_response), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            error_response = {"status": "error", "message": str(e), "data": {}}
            return request.make_response(json.dumps(error_response), headers=[('Content-Type', 'application/json')])