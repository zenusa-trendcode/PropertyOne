# User Guide PropertiOne PMS

Panduan ini ditujukan untuk pengguna operasional PropertiOne PMS: property manager, finance AR, facility team, admin dokumen, owner representative, dan manajemen yang memantau portfolio properti.

## 1. Gambaran Sistem

PropertiOne PMS adalah sistem property management untuk mengelola proses bisnis utama:

- Portfolio properti
- Unit dan status okupansi
- Tenant dan kelengkapan KYC
- Lease/kontrak sewa
- Billing, invoice, payment, dan aging piutang
- Maintenance/work order
- Inspection dan finding
- Document vault
- Approval request
- Report untuk owner dan internal team

Sistem dibuat agar tim operasional dapat melihat kondisi portfolio, mengambil tindakan harian, dan menjaga data sewa/pembayaran/maintenance tetap rapi.

## 2. Login

Buka aplikasi melalui:

```text
http://127.0.0.1:8000/
```

Akun demo:

```text
Username: admin
Password: Admin12345!
```

Setelah login, pengguna akan masuk ke halaman **Command Center**.

## 3. Navigasi Utama

Navigasi berada di sisi kiri layar.

Menu utama:

- **Command Center**: dashboard utama seluruh operasi.
- **Organizations**: data perusahaan/operator/owner.
- **Properties**: master data properti.
- **Units**: daftar unit, status, harga sewa, dan kondisi unit.
- **Tenants**: data penyewa, KYC, risiko, dan outstanding balance.
- **Leases**: kontrak sewa, masa berlaku, deposit, dan renewal.
- **Billing**: invoice, status pembayaran, dan aging piutang.
- **Vendors**: vendor maintenance dan SLA.
- **Maintenance**: work order, vendor assignment, approval, dan status pekerjaan.
- **Inspections**: jadwal inspeksi, score, dan finding.
- **Documents**: dokumen lease, KYC, handover, insurance, tax, dan compliance.
- **Approvals**: permintaan approval untuk capex, write-off, diskon, atau exception.
- **Reports**: paket laporan untuk owner, finance, dan facility.

## 4. Command Center

Command Center adalah halaman utama untuk melihat kondisi portfolio.

KPI yang tersedia:

- **Monthly Rent Roll**: total sewa aktif dari lease berjalan.
- **Occupancy**: persentase unit yang terisi.
- **Outstanding AR**: piutang yang belum lunas.
- **Open Work Orders**: pekerjaan maintenance yang belum selesai.
- **Deposit Held**: total deposit dari lease aktif/renewal.
- **Approvals**: approval yang masih pending.

Panel utama:

- **Portfolio Performance**: performa tiap properti.
- **Cash Aging**: jumlah dan nilai invoice berdasarkan umur piutang.
- **Priority Queue**: work order prioritas.
- **Lease Pipeline**: kontrak aktif, renewal, notice, dan collection hold.
- **Documents Due**: dokumen yang belum lengkap atau mendekati expiry.
- **Approval Queue**: approval yang perlu keputusan.
- **Activity Timeline**: aktivitas terbaru sistem.

Tips penggunaan:

- Gunakan filter **Property** di kanan atas untuk fokus pada satu properti.
- Klik nama properti, invoice, work order, lease, atau dokumen untuk membuka detail.
- Gunakan tombol **Reports** untuk membuka pusat laporan.

## 5. Mengelola Property

Menu: **Properties**

Gunakan modul ini untuk menyimpan data master properti:

- Kode properti
- Nama properti
- Jenis properti
- Status operasional
- Alamat dan kota
- Property manager
- Gross area dan net leasable area
- Service charge rate
- Sinking fund rate
- Tanggal statement owner

Workflow umum:

1. Buka **Properties**.
2. Klik **+ Add Properties**.
3. Isi data properti.
4. Klik **Save**.
5. Buka detail properti untuk melihat ringkasan unit, rent roll, work order, dan dokumen.

Status property yang disarankan:

- **Active**: properti aktif normal.
- **Stabilized**: okupansi dan cashflow stabil.
- **Lease Up**: properti sedang fase pengisian unit.
- **Watchlist**: properti perlu perhatian khusus.
- **Inactive**: properti tidak aktif.

## 6. Mengelola Unit

Menu: **Units**

Modul unit dipakai untuk mengontrol ketersediaan unit dan kondisi operasional.

Data penting:

- Property
- Unit code
- Floor
- Unit type
- Area
- Bedroom/bathroom
- Status
- Market rent
- Current rent
- Handover state
- Meter listrik dan air
- Next action

Status unit:

- **Vacant**: kosong dan bisa dipasarkan.
- **Make Ready**: sedang dipersiapkan sebelum disewakan.
- **Occupied**: sedang ditempati tenant.
- **Notice**: tenant sudah memberi notice keluar.
- **Delinquent**: tenant menunggak.
- **Offline**: unit tidak bisa disewakan sementara.

Praktik operasional:

- Isi **market rent** sebagai harga referensi pasar.
- Isi **current rent** jika unit sedang disewa.
- Gunakan **next action** untuk mencatat tindakan berikutnya, misalnya `Publish listing`, `Schedule handover`, atau `Payment plan`.

## 7. Mengelola Tenant

Menu: **Tenants**

Modul tenant menyimpan identitas penyewa dan risiko operasional.

Data penting:

- Tenant code
- Tenant type
- Display name
- Legal name
- Tax ID
- Email dan phone
- Billing address
- Risk level
- KYC status
- Tenant health score
- Last contact date
- Notes

Risk level:

- **Excellent**: pembayaran dan dokumen baik.
- **Monitor**: ada isu kecil yang perlu dipantau.
- **At Risk**: risiko tinggi, biasanya terkait tunggakan, dokumen, atau sengketa.

KYC status:

- **Pending**: dokumen belum diterima.
- **Partial**: sebagian dokumen sudah ada.
- **Complete**: dokumen lengkap.
- **Expired**: dokumen perlu diperbarui.

Praktik operasional:

- Update **last contact date** setelah komunikasi penting.
- Gunakan **notes** untuk janji bayar, isu legal, atau informasi khusus tenant.
- Pantau **outstanding balance** dari detail tenant.

## 8. Mengelola Lease

Menu: **Leases**

Lease adalah kontrak antara tenant, unit, dan property.

Data penting:

- Lease code
- Property
- Unit
- Tenant
- Status
- Start date dan end date
- Rent amount
- Deposit amount
- Service charge amount
- Billing cycle
- Escalation type dan rate
- Renewal probability
- Notes

Status lease:

- **Draft**: kontrak sedang disiapkan.
- **Active**: kontrak berjalan.
- **Renewal Offered**: renewal sudah ditawarkan.
- **Move Out Notice**: tenant akan keluar.
- **Collection Hold**: lease bermasalah karena pembayaran.
- **Expired**: kontrak berakhir.
- **Terminated**: kontrak dihentikan.

Workflow renewal:

1. Buka **Leases**.
2. Filter lease yang end date-nya dekat.
3. Buka detail lease.
4. Update status menjadi **Renewal Offered** jika renewal sudah dikirim.
5. Isi renewal probability.
6. Catat negosiasi di notes.

Workflow move-out:

1. Ubah status lease menjadi **Move Out Notice**.
2. Update unit menjadi **Notice**.
3. Buat dokumen BAST/handover di **Documents**.
4. Buat work order make-ready jika perlu.

## 9. Billing dan Collection

Menu: **Billing**

Modul ini dipakai untuk mengelola invoice, payment, outstanding, dan aging piutang.

Data invoice:

- Invoice number
- Property
- Tenant
- Lease
- Line type
- Status
- Issue date
- Due date
- Subtotal
- Tax
- Discount
- Paid amount
- Reminder count
- Notes

Status invoice:

- **Draft**: invoice belum diterbitkan.
- **Issued**: invoice sudah diterbitkan.
- **Partially Paid**: pembayaran sebagian.
- **Paid**: lunas.
- **Overdue**: lewat jatuh tempo.
- **Escalated**: masuk tahap eskalasi collection/legal.
- **Void**: dibatalkan.

Aging bucket:

- **Current**: belum jatuh tempo atau sudah lunas.
- **1-30**: terlambat sampai 30 hari.
- **31-60**: terlambat 31-60 hari.
- **61-90**: terlambat 61-90 hari.
- **90+**: terlambat lebih dari 90 hari.

Workflow collection:

1. Buka **Billing**.
2. Cari invoice dengan status **Overdue** atau **Escalated**.
3. Buka detail invoice.
4. Update reminder count setelah reminder dikirim.
5. Catat janji bayar di notes.
6. Jika perlu approval legal atau write-off, buat request di **Approvals**.

## 10. Maintenance / Work Order

Menu: **Maintenance**

Work order dipakai untuk mencatat dan mengontrol pekerjaan perbaikan, preventive maintenance, dan pekerjaan vendor.

Data penting:

- Work order number
- Property
- Unit
- Tenant
- Vendor
- Title
- Description
- Priority
- Category
- Status
- Reported at
- Due at
- Requester
- Estimated cost
- Approved budget
- Actual cost
- Owner approval flag
- Before/after photo requirement

Priority:

- **Low**
- **Medium**
- **High**
- **Emergency**
- **Preventive**

Status workflow:

- **New**
- **Triaged**
- **Waiting Approval**
- **Vendor Assigned**
- **Waiting Parts**
- **In Progress**
- **QA Review**
- **Closed**
- **Cancelled**

Quick transition:

Pada halaman detail work order, tersedia tombol:

- Vendor Assigned
- In Progress
- QA Review
- Close Work Order

Setiap perubahan status otomatis membuat activity event.

Workflow maintenance:

1. Buka **Maintenance**.
2. Klik **+ Add Maintenance**.
3. Isi property, unit/tenant jika relevan, judul, deskripsi, prioritas, dan due date.
4. Jika biaya tinggi, aktifkan **requires owner approval**.
5. Assign vendor.
6. Gunakan quick transition sampai status **Closed**.

Praktik operasional:

- Jangan close work order sebelum evidence lengkap.
- Gunakan field **estimated cost**, **approved budget**, dan **actual cost** untuk kontrol biaya.
- Emergency work order sebaiknya memiliki due date dalam hitungan jam.

## 11. Vendors

Menu: **Vendors**

Modul vendor menyimpan data pihak ketiga yang mengerjakan maintenance.

Data penting:

- Vendor code
- Name
- Category
- Contact person
- Phone
- Email
- SLA hours
- Rating
- Active status

Praktik operasional:

- Gunakan SLA hours untuk memilih vendor sesuai urgensi.
- Nonaktifkan vendor yang sudah tidak dipakai.
- Update rating berdasarkan kualitas pekerjaan dan ketepatan SLA.

## 12. Inspections

Menu: **Inspections**

Inspection dipakai untuk jadwal pemeriksaan properti/unit dan compliance.

Data penting:

- Inspection number
- Property
- Unit
- Scope
- Status
- Scheduled date
- Completed date
- Inspector
- Score
- Notes

Status inspection:

- **Scheduled**
- **In Progress**
- **Needs Action**
- **Critical**
- **Complete**

Workflow inspection:

1. Buat jadwal inspection.
2. Isi scope, inspector, dan scheduled date.
3. Setelah pemeriksaan, update score dan notes.
4. Jika ada temuan, catat finding melalui admin atau pengembangan lanjutan form finding.
5. Buat work order jika finding butuh tindakan teknis.

## 13. Documents

Menu: **Documents**

Document vault menyimpan metadata dokumen penting.

Jenis dokumen:

- Lease
- Tenant KYC
- Handover
- Asset
- Insurance
- Tax
- Vendor
- Other

Status dokumen:

- **Draft**
- **Pending**
- **Review**
- **Complete**
- **Expired**

Workflow dokumen:

1. Buka **Documents**.
2. Klik **+ Add Documents**.
3. Pilih property, tenant, atau lease yang terkait.
4. Isi document number, title, type, owner, expiry date, dan notes.
5. Update status menjadi **Complete** setelah dokumen final tersedia.

Praktik operasional:

- Gunakan expiry date untuk dokumen insurance, tax, permit, dan compliance.
- Dokumen tenant KYC yang pending harus dipantau dari Command Center.
- Untuk produksi komersial, fitur upload file asli dapat ditambahkan di tahap berikutnya.

## 14. Approvals

Menu: **Approvals**

Approval dipakai untuk tindakan yang butuh persetujuan manager/owner.

Contoh approval:

- Capex maintenance
- Diskon renewal
- Write-off invoice
- Legal collection notice
- Lease exception
- Vendor cost over budget

Data penting:

- Request number
- Property
- Object type
- Object reference
- Title
- Requested by
- Approver name
- Amount
- Status
- Due date
- Decision note

Status approval:

- **Pending**
- **Approved**
- **Rejected**
- **Cancelled**

Workflow approval:

1. Buat approval request dari menu **Approvals**.
2. Isi object reference, misalnya `WO-1045` atau `INV-0726-044`.
3. Masukkan amount dan approver.
4. Setelah keputusan dibuat, update status dan decision note.

## 15. Reports

Menu: **Reports**

Paket laporan yang tersedia:

- **Owner Statement**: rent roll, NOI, deposit held, owner payout.
- **Delinquency Pack**: outstanding, aging bucket, reminder, commitment.
- **Asset Health**: open WO, SLA breach, inspection score, vendor rating.
- **Lease Expiry Book**: expiry, renewal probability, market rent gap, make-ready date.

Pada versi saat ini, tombol **Generate** adalah placeholder UI. Untuk produk komersial, tahap berikutnya adalah membuat export PDF/XLSX.

## 16. Django Admin

Admin tersedia di:

```text
http://127.0.0.1:8000/admin/
```

Gunakan akun:

```text
Username: admin
Password: Admin12345!
```

Django Admin berguna untuk:

- Melihat semua model data.
- Mengedit data yang belum punya UI khusus.
- Mengelola inspection finding.
- Mengelola user internal.
- Debug data saat implementasi awal.

## 17. Workflow Harian yang Disarankan

### Property Manager

1. Buka Command Center.
2. Filter property yang menjadi tanggung jawab.
3. Cek occupancy, open work order, dan approval pending.
4. Buka Lease Pipeline untuk kontrak yang perlu renewal.
5. Cek Documents Due.
6. Follow up tenant at risk.

### Finance AR

1. Buka Billing.
2. Filter invoice overdue.
3. Cek aging bucket dan outstanding amount.
4. Update reminder count dan notes.
5. Buat approval untuk legal escalation jika perlu.
6. Cek report Delinquency Pack.

### Facility Team

1. Buka Maintenance.
2. Prioritaskan Emergency dan High.
3. Assign vendor sesuai SLA.
4. Update status work order.
5. Cek inspection critical.
6. Close work order setelah evidence lengkap.

### Owner Representative

1. Buka Command Center.
2. Cek rent roll, occupancy, outstanding, dan deposit held.
3. Review approval pending.
4. Buka Reports untuk Owner Statement dan Asset Health.

## 18. Aturan Data yang Perlu Dijaga

- Setiap property harus punya kode unik.
- Setiap unit unik dalam satu property.
- Lease harus menghubungkan property, unit, dan tenant yang benar.
- Invoice sebaiknya selalu terkait tenant dan property.
- Work order emergency harus punya due date jelas.
- Approval wajib dibuat untuk biaya besar, diskon besar, atau tindakan legal.
- Dokumen compliance harus punya expiry date.
- Tenant risk harus diperbarui jika ada tunggakan atau dokumen bermasalah.

## 19. Batasan Versi Saat Ini

Versi ini sudah berjalan sebagai aplikasi Django dengan database dan CRUD inti, tetapi beberapa fitur komersial masih perlu ditambahkan sebelum dijual luas:

- Role-based access control per modul dan per property.
- Multi-company tenancy untuk banyak client.
- Upload file dokumen asli.
- Export PDF/XLSX.
- Email/WhatsApp reminder otomatis.
- Payment gateway atau bank statement matching.
- Audit trail detail per perubahan field.
- Dashboard owner portal terpisah.
- API integration untuk mobile app atau tenant portal.
- Production deployment dengan PostgreSQL, object storage, backup, dan monitoring.

## 20. Troubleshooting

Jika aplikasi tidak bisa dibuka:

1. Pastikan server berjalan:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

2. Pastikan database sudah dimigrasi:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

3. Jika data demo belum ada:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo
```

4. Jika login gagal, jalankan ulang seed demo untuk reset password admin:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo
```

5. Untuk cek kesehatan sistem:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```
