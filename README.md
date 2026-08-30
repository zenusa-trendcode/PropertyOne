# PropertiOne PMS

PropertiOne PMS adalah prototype property management system berbasis Vinext/React untuk mengelola portfolio properti, unit, tenant, lease, billing, maintenance, inspeksi, dokumen, report, dan role approval dalam satu dashboard operasional.

## Modul utama

- Command Center: KPI portfolio, rent roll, occupancy, outstanding, work order, cash aging, dan activity timeline.
- Portfolio: health card per properti dengan occupancy, inspection score, service score, NOI, deposit held, dan risk status.
- Units: daftar unit, status vacancy, lease end, kondisi unit, meter check, rent, dan next action.
- Tenants: tenant health, saldo, dokumen, last contact, dan communication log.
- Leases: pipeline Active, Renewal Offered, Move Out Notice, dan Collection Hold dengan probability renewal.
- Billing: accounts receivable, paid amount, outstanding, aging bucket, dan collection playbook.
- Maintenance: kanban work order berdasarkan state, priority, SLA, vendor, dan biaya.
- Inspections: kalender inspeksi, score, finding, compliance checklist.
- Documents: vault dokumen legal, compliance, handover, asset, owner, expiry, dan status.
- Reports and Settings: report pack owner/finance/facility serta matrix role dan business rules.

## Menjalankan proyek

```bash
npm install
npm run dev
```

Preview lokal akan tersedia di `http://localhost:3000/`.

## Build produksi

```bash
npm run build
```

Stack proyek mengikuti scaffold Sites/Vinext: Next-style `app/`, React 19, TypeScript, Vite, Tailwind CSS, dan Cloudflare Worker-compatible output.
