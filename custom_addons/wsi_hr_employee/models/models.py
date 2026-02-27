from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    # Menginherit model yang sudah ada
    _inherit = 'hr.employee'
    # Menambahkan field NIP
    employee_id = fields.Char(string='Employee ID')
    date_joined = fields.Date(string='Date Joined')
    employee_tenure = fields.Char(string='Employee Tenure', compute='_compute_employee_tenure', store=False)

    @api.depends('date_joined') 
    def _compute_employee_tenure(self):
        for record in self:
            # Cek apakah tanggal_bergabung sudah diisi oleh user
            if record.date_joined:
                # Ambil tanggal hari ini
                today = fields.Date.today()
                
                # Hitung selisih tanggal menggunakan relativedelta
                selisih = relativedelta(today, record.date_joined)
                
                # Format hasilnya menjadi teks "X Tahun, Y Bulan, Z Hari"
                record.employee_tenure = f"{selisih.years} Years, {selisih.months} Months, {selisih.days} Days"
            else:
                # Jika tanggal bergabung masih kosong
                record.employee_tenure = "No data yet"