from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    # Menginherit model yang sudah ada
    _inherit = 'hr.employee'
    # Menambahkan field NIP
    employee_id = fields.Char(string='Employee ID', compute='_compute_employee_id', store=True)
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
    
    @api.depends('date_joined')
    def _compute_employee_id(self):
        # Hitung total karyawan yang sudah ada di database saat ini
        # Ini diletakkan di luar 'for' agar aman saat Anda melakukan import/load data massal
        base_count = self.env['hr.employee'].search_count([])
        
        for index, record in enumerate(self):
            # PENCEGAHAN: Jika record sudah punya Employee ID, lewati (jangan diubah lagi)
            if record.employee_id:
                continue
                
            # A. TANGGAL DIBUAT (Format: DDMMYYYY)
            # Jika punya tanggal pembuatan sistem, gunakan itu (untuk load data lama), jika tidak gunakan hari ini
            if record.create_date:
                tgl_buat = record.create_date.strftime('%d%m%Y')
            else:
                tgl_buat = fields.Date.today().strftime('%d%m%Y')
                
            # B. TAHUN MASUK (Format: YYYY)
            if record.date_joined:
                tahun_masuk = record.date_joined.strftime('%Y')
            else:
                # Jika HRD lupa mengisi date_joined, default ke tahun ini
                tahun_masuk = fields.Date.today().strftime('%Y') 
                
            # C. URUTAN KARYAWAN (Karyawan ke-X)
            # base_count + index (urutan baris saat import) + 1
            urutan = base_count + index + 1
            
            # GABUNGKAN SEMUANYA
            record.employee_id = f"{tgl_buat}{tahun_masuk}{urutan}"