# PropertiOne PMS

PropertiOne PMS adalah property management system full-stack berbasis Django untuk kebutuhan bisnis nyata: portfolio, unit, tenant, lease, billing, maintenance, inspection, document vault, approval, reporting, dan dashboard operasional.

## Dokumentasi

- [User Guide](USER_GUIDE.md): panduan penggunaan untuk property manager, finance, facility, owner representative, dan admin.

## Cara run

```powershell
cd "C:\Users\Artha-12\OneDrive - Artha Data Solutions LLC\Documents\Zenusa\Property Management System"
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Buka `http://127.0.0.1:8000/`.

## Login demo

- Username: `admin`
- Password: `Admin12345!`

## Setup ulang dari awal

Jika database belum ada atau proyek dipindahkan ke komputer lain:

```powershell
cd "C:\Users\Artha-12\OneDrive - Artha Data Solutions LLC\Documents\Zenusa\Property Management System"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

## Modul produk

- Command Center: KPI rent roll, occupancy, outstanding AR, deposit held, open work order, approval queue, lease pipeline, activity timeline.
- Organizations: legal entity, tax, currency, contact, dan ownership context.
- Properties: property master, manager, service charge, sinking fund, occupancy, rent roll.
- Units: status availability, market rent, current rent, handover, meter, next action.
- Tenants: KYC, tenant health, risk level, contact, outstanding balance.
- Leases: active lease, renewal, notice, collection hold, rent, deposit, escalation, renewal probability.
- Billing: invoice, payment, outstanding, aging bucket, reminder count.
- Vendors: vendor category, SLA, rating, contact, active status.
- Maintenance: work order, priority, SLA, vendor assignment, owner approval, evidence rules, quick status transition.
- Inspections: schedule, score, finding, corrective action.
- Documents: legal/KYC/handover/insurance/tax vault, expiry monitoring, owner.
- Approvals: capex, collection, discount, exception approval flow.
- Reports: owner statement, delinquency pack, asset health, lease expiry book.

## Verifikasi

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

Keduanya sudah lulus pada implementasi saat ini.
