'use client';

import { type CSSProperties, useMemo, useState } from 'react';

type ModuleKey =
  | 'command'
  | 'portfolio'
  | 'units'
  | 'tenants'
  | 'leases'
  | 'billing'
  | 'maintenance'
  | 'inspections'
  | 'documents'
  | 'reports'
  | 'settings';

const navSections: { title: string; items: { key: ModuleKey; label: string; code: string }[] }[] = [
  {
    title: 'Operations',
    items: [
      { key: 'command', label: 'Command Center', code: 'CC' },
      { key: 'portfolio', label: 'Portfolio', code: 'PF' },
      { key: 'units', label: 'Units', code: 'UN' },
      { key: 'tenants', label: 'Tenants', code: 'TN' },
      { key: 'leases', label: 'Leases', code: 'LS' },
    ],
  },
  {
    title: 'Execution',
    items: [
      { key: 'billing', label: 'Billing', code: 'BL' },
      { key: 'maintenance', label: 'Maintenance', code: 'MT' },
      { key: 'inspections', label: 'Inspections', code: 'IN' },
      { key: 'documents', label: 'Documents', code: 'DC' },
    ],
  },
  {
    title: 'Control',
    items: [
      { key: 'reports', label: 'Reports', code: 'RP' },
      { key: 'settings', label: 'Settings', code: 'ST' },
    ],
  },
];

const properties = [
  {
    id: 'kemang',
    name: 'Artha Residence Kemang',
    category: 'Apartemen',
    area: 'Jakarta Selatan',
    address: 'Jl. Kemang Raya 18',
    manager: 'Maya Putri',
    units: 128,
    occupied: 121,
    rentRoll: 1820000000,
    arrears: 38400000,
    noi: 642000000,
    deposits: 4120000000,
    openTickets: 9,
    expiringLeases: 7,
    inspectionScore: 93,
    serviceScore: 91,
    risk: 'Stabil',
    mix: 'Studio, 1BR, 2BR',
  },
  {
    id: 'bsd',
    name: 'Nusa Office Park',
    category: 'Komersial',
    area: 'BSD City',
    address: 'Green Office Boulevard Kav. 6',
    manager: 'Rizky Pratama',
    units: 64,
    occupied: 56,
    rentRoll: 2440000000,
    arrears: 162000000,
    noi: 880000000,
    deposits: 5150000000,
    openTickets: 17,
    expiringLeases: 11,
    inspectionScore: 86,
    serviceScore: 79,
    risk: 'Perlu Follow Up',
    mix: 'Retail, Office, Storage',
  },
  {
    id: 'serpong',
    name: 'Serpong Garden Cluster',
    category: 'Townhouse',
    area: 'Tangerang Selatan',
    address: 'Cluster Gardenia Blok A',
    manager: 'Dewi Lestari',
    units: 42,
    occupied: 34,
    rentRoll: 746000000,
    arrears: 70100000,
    noi: 211000000,
    deposits: 1280000000,
    openTickets: 8,
    expiringLeases: 5,
    inspectionScore: 82,
    serviceScore: 84,
    risk: 'At Risk',
    mix: '2BR, 3BR, Corner Lot',
  },
  {
    id: 'canggu',
    name: 'Canggu Living Suites',
    category: 'Serviced Villa',
    area: 'Badung',
    address: 'Jl. Pantai Batu Bolong 42',
    manager: 'Made Ari',
    units: 27,
    occupied: 25,
    rentRoll: 1190000000,
    arrears: 12800000,
    noi: 498000000,
    deposits: 970000000,
    openTickets: 3,
    expiringLeases: 2,
    inspectionScore: 96,
    serviceScore: 94,
    risk: 'Stabil',
    mix: 'Villa, Suite, Long Stay',
  },
];

const units = [
  {
    id: 'A-1207',
    propertyId: 'kemang',
    floor: '12',
    type: '2BR',
    size: 72,
    status: 'Occupied',
    tenant: 'Nadia Hartono',
    rent: 18500000,
    leaseEnd: '2026-10-31',
    condition: 'Good',
    meter: 'Normal',
    nextAction: 'Renewal call',
  },
  {
    id: 'B-0811',
    propertyId: 'kemang',
    floor: '08',
    type: 'Studio',
    size: 32,
    status: 'Notice',
    tenant: 'Kenji Tan',
    rent: 8700000,
    leaseEnd: '2026-09-18',
    condition: 'Need paint',
    meter: 'Check water',
    nextAction: 'Schedule handover',
  },
  {
    id: 'R-03',
    propertyId: 'bsd',
    floor: 'GF',
    type: 'Retail',
    size: 110,
    status: 'Occupied',
    tenant: 'Kopi Lajur Selatan',
    rent: 52000000,
    leaseEnd: '2027-02-28',
    condition: 'Good',
    meter: 'Normal',
    nextAction: 'VAT document',
  },
  {
    id: 'O-1702',
    propertyId: 'bsd',
    floor: '17',
    type: 'Office',
    size: 240,
    status: 'Vacant',
    tenant: '-',
    rent: 88000000,
    leaseEnd: '-',
    condition: 'Ready',
    meter: 'Normal',
    nextAction: 'Publish listing',
  },
  {
    id: 'G-12',
    propertyId: 'serpong',
    floor: 'Cluster',
    type: '3BR',
    size: 138,
    status: 'Delinquent',
    tenant: 'Bima Santoso',
    rent: 15500000,
    leaseEnd: '2026-12-15',
    condition: 'Minor leak',
    meter: 'Normal',
    nextAction: 'Payment plan',
  },
  {
    id: 'V-09',
    propertyId: 'canggu',
    floor: 'Villa',
    type: 'Suite',
    size: 95,
    status: 'Occupied',
    tenant: 'Oceanlane Studio',
    rent: 42000000,
    leaseEnd: '2027-04-30',
    condition: 'Excellent',
    meter: 'Normal',
    nextAction: 'Guest compliance',
  },
];

const tenants = [
  {
    id: 'T-1001',
    name: 'Nadia Hartono',
    segment: 'Residential',
    propertyId: 'kemang',
    unit: 'A-1207',
    rent: 18500000,
    balance: 0,
    health: 96,
    status: 'Excellent',
    lastContact: '2026-08-28',
    documents: 'Complete',
  },
  {
    id: 'T-1002',
    name: 'Kopi Lajur Selatan',
    segment: 'Retail F&B',
    propertyId: 'bsd',
    unit: 'R-03',
    rent: 52000000,
    balance: 12000000,
    health: 82,
    status: 'Monitor',
    lastContact: '2026-08-25',
    documents: 'NIB pending',
  },
  {
    id: 'T-1003',
    name: 'Bima Santoso',
    segment: 'Residential',
    propertyId: 'serpong',
    unit: 'G-12',
    rent: 15500000,
    balance: 46500000,
    health: 58,
    status: 'At Risk',
    lastContact: '2026-08-21',
    documents: 'Deposit review',
  },
  {
    id: 'T-1004',
    name: 'Oceanlane Studio',
    segment: 'Creative Office',
    propertyId: 'canggu',
    unit: 'V-09',
    rent: 42000000,
    balance: 0,
    health: 91,
    status: 'Excellent',
    lastContact: '2026-08-26',
    documents: 'Complete',
  },
];

const leases = [
  {
    id: 'LS-24031',
    tenant: 'Nadia Hartono',
    propertyId: 'kemang',
    unit: 'A-1207',
    start: '2025-11-01',
    end: '2026-10-31',
    rent: 18500000,
    deposit: 37000000,
    escalation: '5% annual',
    stage: 'Renewal Offered',
    probability: 72,
    action: 'Negotiate 2-year term',
  },
  {
    id: 'LS-24028',
    tenant: 'Kenji Tan',
    propertyId: 'kemang',
    unit: 'B-0811',
    start: '2025-09-19',
    end: '2026-09-18',
    rent: 8700000,
    deposit: 17400000,
    escalation: 'Fixed',
    stage: 'Move Out Notice',
    probability: 18,
    action: 'Prepare make-ready',
  },
  {
    id: 'LS-23012',
    tenant: 'Kopi Lajur Selatan',
    propertyId: 'bsd',
    unit: 'R-03',
    start: '2024-03-01',
    end: '2027-02-28',
    rent: 52000000,
    deposit: 156000000,
    escalation: 'CPI capped 8%',
    stage: 'Active',
    probability: 88,
    action: 'Collect NIB update',
  },
  {
    id: 'LS-25004',
    tenant: 'Bima Santoso',
    propertyId: 'serpong',
    unit: 'G-12',
    start: '2025-12-16',
    end: '2026-12-15',
    rent: 15500000,
    deposit: 31000000,
    escalation: '5% annual',
    stage: 'Collection Hold',
    probability: 42,
    action: 'Payment commitment',
  },
  {
    id: 'LS-25017',
    tenant: 'Oceanlane Studio',
    propertyId: 'canggu',
    unit: 'V-09',
    start: '2026-05-01',
    end: '2027-04-30',
    rent: 42000000,
    deposit: 84000000,
    escalation: '6% annual',
    stage: 'Active',
    probability: 91,
    action: 'Guest usage audit',
  },
];

const invoices = [
  {
    id: 'INV-0826-001',
    tenant: 'Kopi Lajur Selatan',
    propertyId: 'bsd',
    due: '2026-08-15',
    amount: 52000000,
    paid: 40000000,
    aging: '1-30',
    status: 'Partially Paid',
  },
  {
    id: 'INV-0826-008',
    tenant: 'Bima Santoso',
    propertyId: 'serpong',
    due: '2026-07-31',
    amount: 15500000,
    paid: 0,
    aging: '31-60',
    status: 'Overdue',
  },
  {
    id: 'INV-0726-044',
    tenant: 'Bima Santoso',
    propertyId: 'serpong',
    due: '2026-07-01',
    amount: 15500000,
    paid: 0,
    aging: '61-90',
    status: 'Escalated',
  },
  {
    id: 'INV-0826-011',
    tenant: 'Nadia Hartono',
    propertyId: 'kemang',
    due: '2026-08-10',
    amount: 18500000,
    paid: 18500000,
    aging: 'Current',
    status: 'Paid',
  },
  {
    id: 'INV-0826-020',
    tenant: 'Oceanlane Studio',
    propertyId: 'canggu',
    due: '2026-08-20',
    amount: 42000000,
    paid: 42000000,
    aging: 'Current',
    status: 'Paid',
  },
];

const workOrders = [
  {
    id: 'WO-1048',
    title: 'AC bocor unit A-1207',
    propertyId: 'kemang',
    unit: 'A-1207',
    priority: 'Emergency',
    state: 'Vendor Assigned',
    assignee: 'CoolPro HVAC',
    sla: '04:20',
    cost: 1250000,
  },
  {
    id: 'WO-1047',
    title: 'Lift tower A inspeksi bulanan',
    propertyId: 'kemang',
    unit: 'Common Area',
    priority: 'Preventive',
    state: 'Scheduled',
    assignee: 'Kone Service',
    sla: '2d',
    cost: 0,
  },
  {
    id: 'WO-1045',
    title: 'Pompa transfer basement',
    propertyId: 'bsd',
    unit: 'B2 Pump Room',
    priority: 'High',
    state: 'Waiting Parts',
    assignee: 'Facility Team',
    sla: '13:10',
    cost: 8700000,
  },
  {
    id: 'WO-1043',
    title: 'Cat ulang koridor lantai 9',
    propertyId: 'kemang',
    unit: 'L9 Corridor',
    priority: 'Medium',
    state: 'In Progress',
    assignee: 'In-house',
    sla: '5d',
    cost: 3400000,
  },
  {
    id: 'WO-1039',
    title: 'Kebocoran dak carport',
    propertyId: 'serpong',
    unit: 'G-12',
    priority: 'High',
    state: 'Diagnosing',
    assignee: 'Vendor roof',
    sla: '18:45',
    cost: 0,
  },
];

const inspections = [
  {
    id: 'INSP-081',
    propertyId: 'kemang',
    scope: 'Fire safety and hydrant',
    due: '2026-09-03',
    score: 92,
    status: 'Scheduled',
    findings: 3,
  },
  {
    id: 'INSP-076',
    propertyId: 'bsd',
    scope: 'Retail signage compliance',
    due: '2026-09-05',
    score: 78,
    status: 'Needs Action',
    findings: 8,
  },
  {
    id: 'INSP-072',
    propertyId: 'serpong',
    scope: 'Roof and gutter survey',
    due: '2026-08-31',
    score: 69,
    status: 'Critical',
    findings: 12,
  },
  {
    id: 'INSP-067',
    propertyId: 'canggu',
    scope: 'Guest safety checklist',
    due: '2026-09-02',
    score: 96,
    status: 'Ready',
    findings: 1,
  },
];

const documents = [
  {
    id: 'DOC-221',
    name: 'Lease agreement signed',
    entity: 'LS-24031 / Nadia Hartono',
    type: 'Legal',
    status: 'Complete',
    owner: 'Legal Ops',
    expiry: '2026-10-31',
  },
  {
    id: 'DOC-219',
    name: 'Tenant NIB and tax profile',
    entity: 'Kopi Lajur Selatan',
    type: 'Compliance',
    status: 'Pending',
    owner: 'Account Manager',
    expiry: '2026-09-07',
  },
  {
    id: 'DOC-211',
    name: 'BAST move-out checklist',
    entity: 'B-0811 / Kenji Tan',
    type: 'Handover',
    status: 'Draft',
    owner: 'Property Admin',
    expiry: '2026-09-18',
  },
  {
    id: 'DOC-204',
    name: 'Insurance building policy',
    entity: 'Nusa Office Park',
    type: 'Asset',
    status: 'Review',
    owner: 'Finance',
    expiry: '2026-12-01',
  },
];

const activity = [
  ['08:10', 'Payment received', 'Oceanlane Studio membayar invoice Agustus penuh.'],
  ['09:25', 'Work order escalated', 'WO-1048 butuh vendor HVAC hari ini.'],
  ['10:40', 'Lease renewal', 'Nadia Hartono meminta opsi kontrak 24 bulan.'],
  ['13:15', 'Inspection alert', 'Serpong Garden roof survey berada di bawah ambang skor.'],
];

const reportPacks = [
  ['Owner Statement', 'NOI, rent roll, escrow, reserve, dan payout owner.'],
  ['Delinquency Pack', 'Aging, call notes, commitment, dan legal escalation.'],
  ['Asset Health', 'SLA, recurring fault, capex forecast, dan vendor score.'],
  ['Lease Expiry Book', 'Rolling 30/60/90 hari dengan renewal probability.'],
];

const roles = [
  ['Property Manager', 'Approve work order sampai Rp 10Jt, renewal, dan write-off kecil.'],
  ['Finance AR', 'Posting invoice, payment matching, aging, dan reminder.'],
  ['Facility Lead', 'Assign vendor, inspect asset, close maintenance evidence.'],
  ['Owner Viewer', 'Read-only portfolio, statement, occupancy, dan capex.'],
];

const allNavItems = navSections.flatMap((section) => section.items);

function money(value: number) {
  return new Intl.NumberFormat('id-ID', {
    currency: 'IDR',
    maximumFractionDigits: 0,
    style: 'currency',
  }).format(value);
}

function compactMoney(value: number) {
  if (value >= 1000000000) {
    return `Rp ${(value / 1000000000).toFixed(2)}M`;
  }
  if (value >= 1000000) {
    return `Rp ${Math.round(value / 1000000)}Jt`;
  }
  return money(value);
}

function occupancy(property: (typeof properties)[number]) {
  return Math.round((property.occupied / property.units) * 100);
}

function statusTone(status: string) {
  const lower = status.toLowerCase();
  if (lower.includes('risk') || lower.includes('critical') || lower.includes('overdue') || lower.includes('escalated')) {
    return 'danger';
  }
  if (lower.includes('follow') || lower.includes('pending') || lower.includes('notice') || lower.includes('review') || lower.includes('monitor')) {
    return 'warning';
  }
  if (lower.includes('paid') || lower.includes('complete') || lower.includes('stabil') || lower.includes('ready') || lower.includes('excellent')) {
    return 'success';
  }
  return 'neutral';
}

export default function Home() {
  const [activeModule, setActiveModule] = useState<ModuleKey>('command');
  const [selectedPropertyId, setSelectedPropertyId] = useState('all');
  const [query, setQuery] = useState('');

  const selectedProperty = properties.find((property) => property.id === selectedPropertyId);
  const scopedProperties = selectedProperty ? [selectedProperty] : properties;
  const loweredQuery = query.trim().toLowerCase();

  const scopedUnits = useMemo(() => {
    return units.filter((unit) => {
      const inProperty = selectedPropertyId === 'all' || unit.propertyId === selectedPropertyId;
      const inSearch = [unit.id, unit.type, unit.tenant, unit.status, unit.nextAction]
        .join(' ')
        .toLowerCase()
        .includes(loweredQuery);
      return inProperty && inSearch;
    });
  }, [loweredQuery, selectedPropertyId]);

  const scopedInvoices = invoices.filter(
    (invoice) => selectedPropertyId === 'all' || invoice.propertyId === selectedPropertyId,
  );
  const scopedWorkOrders = workOrders.filter(
    (order) => selectedPropertyId === 'all' || order.propertyId === selectedPropertyId,
  );
  const activeTitle = allNavItems.find((item) => item.key === activeModule)?.label ?? 'Command Center';
  const totalRentRoll = scopedProperties.reduce((sum, property) => sum + property.rentRoll, 0);
  const totalArrears = scopedInvoices.reduce((sum, invoice) => sum + Math.max(invoice.amount - invoice.paid, 0), 0);
  const totalUnits = scopedProperties.reduce((sum, property) => sum + property.units, 0);
  const totalOccupied = scopedProperties.reduce((sum, property) => sum + property.occupied, 0);
  const portfolioOccupancy = Math.round((totalOccupied / totalUnits) * 100);
  const openTickets = scopedWorkOrders.length;
  const atRiskTenants = tenants.filter((tenant) => tenant.status === 'At Risk').length;

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">P1</div>
          <div>
            <p className="eyebrow">Property Management System</p>
            <h1>PropertiOne PMS</h1>
          </div>
        </div>
        <div className="topbar-actions">
          <label className="global-search">
            <span aria-hidden="true">Q</span>
            <input
              aria-label="Cari data operasional"
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Cari unit, tenant, invoice, work order"
              value={query}
            />
          </label>
          <button className="icon-button" type="button" aria-label="Buka notifikasi">
            !
          </button>
          <button className="user-pill" type="button">
            Artha Ops
          </button>
        </div>
      </header>

      <aside className="sidebar">
        <div>
          {navSections.map((section) => (
            <nav className="nav-group" key={section.title} aria-label={section.title}>
              <p className="nav-title">{section.title}</p>
              {section.items.map((item) => (
                <button
                  className={activeModule === item.key ? 'nav-item active' : 'nav-item'}
                  key={item.key}
                  onClick={() => setActiveModule(item.key)}
                  type="button"
                >
                  <span>{item.code}</span>
                  {item.label}
                </button>
              ))}
            </nav>
          ))}
        </div>
        <div className="sidebar-card">
          <div>
            <strong>Renewal Watch</strong>
            <span>25 lease expire dalam 90 hari</span>
          </div>
          <div className="mini-meter">
            <i style={{ width: '72%' }} />
          </div>
        </div>
      </aside>

      <section className="content">
        <div className="page-head">
          <div>
            <p className="breadcrumbs">Beranda / {activeTitle}</p>
            <h2>{activeTitle}</h2>
            <p className="page-subtitle">
              Kontrol portfolio, lease, tenant, billing, maintenance, inspeksi, dokumen, dan approval dalam satu workspace.
            </p>
          </div>
          <div className="head-actions">
            <label className="select-control">
              <span>Property</span>
              <select value={selectedPropertyId} onChange={(event) => setSelectedPropertyId(event.target.value)}>
                <option value="all">All Properties</option>
                {properties.map((property) => (
                  <option value={property.id} key={property.id}>
                    {property.name}
                  </option>
                ))}
              </select>
            </label>
            <button className="btn secondary" type="button">
              Export
            </button>
            <button className="btn primary" type="button">
              + New Lease
            </button>
          </div>
        </div>

        <section className="summary-grid" aria-label="Ringkasan portfolio">
          <MetricCard label="Monthly Rent Roll" value={compactMoney(totalRentRoll)} detail="+8.4% vs bulan lalu" />
          <MetricCard label="Occupancy" value={`${portfolioOccupancy}%`} detail={`${totalOccupied} dari ${totalUnits} unit aktif`} />
          <MetricCard label="Outstanding" value={compactMoney(totalArrears)} detail={`${scopedInvoices.length} invoice terpantau`} tone="warning" />
          <MetricCard label="Open Work Orders" value={openTickets.toString()} detail={`${atRiskTenants} tenant at risk`} tone="danger" />
        </section>

        {activeModule === 'command' && (
          <CommandCenter
            properties={scopedProperties}
            invoices={scopedInvoices}
            workOrders={scopedWorkOrders}
          />
        )}
        {activeModule === 'portfolio' && <PortfolioModule properties={scopedProperties} />}
        {activeModule === 'units' && <UnitsModule units={scopedUnits} selectedPropertyId={selectedPropertyId} />}
        {activeModule === 'tenants' && <TenantsModule />}
        {activeModule === 'leases' && <LeasesModule />}
        {activeModule === 'billing' && <BillingModule invoices={scopedInvoices} />}
        {activeModule === 'maintenance' && <MaintenanceModule orders={scopedWorkOrders} />}
        {activeModule === 'inspections' && <InspectionModule />}
        {activeModule === 'documents' && <DocumentsModule />}
        {activeModule === 'reports' && <ReportsModule />}
        {activeModule === 'settings' && <SettingsModule />}
      </section>
    </main>
  );
}

function MetricCard({
  label,
  value,
  detail,
  tone = 'success',
}: {
  label: string;
  value: string;
  detail: string;
  tone?: 'success' | 'warning' | 'danger';
}) {
  return (
    <article className={`summary-card ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

function CommandCenter({
  properties: scopedProperties,
  invoices: scopedInvoices,
  workOrders: scopedWorkOrders,
}: {
  properties: typeof properties;
  invoices: typeof invoices;
  workOrders: typeof workOrders;
}) {
  const agingBuckets = [
    ['Current', scopedInvoices.filter((invoice) => invoice.aging === 'Current').length, '78%'],
    ['1-30', scopedInvoices.filter((invoice) => invoice.aging === '1-30').length, '44%'],
    ['31-60', scopedInvoices.filter((invoice) => invoice.aging === '31-60').length, '31%'],
    ['61-90', scopedInvoices.filter((invoice) => invoice.aging === '61-90').length, '18%'],
  ];

  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Portfolio Performance</h3>
            <p>Okupansi, revenue, ticket, inspeksi, dan risiko per properti.</p>
          </div>
          <button className="btn secondary" type="button">
            View All
          </button>
        </div>
        <PortfolioTable properties={scopedProperties} />
      </section>

      <section className="panel">
        <div className="panel-head compact">
          <h3>Cash Aging</h3>
        </div>
        <div className="aging-list">
          {agingBuckets.map(([label, count, width]) => (
            <div className="aging-row" key={label}>
              <div>
                <strong>{label}</strong>
                <span>{count} invoice</span>
              </div>
              <div className="bar">
                <i style={{ width }} />
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-head compact">
          <h3>Priority Queue</h3>
        </div>
        <div className="work-list">
          {scopedWorkOrders.slice(0, 4).map((order) => (
            <WorkOrderRow order={order} key={order.id} />
          ))}
        </div>
      </section>

      <section className="panel wide">
        <div className="panel-head compact">
          <h3>Activity Timeline</h3>
        </div>
        <div className="timeline">
          {activity.map(([time, title, detail]) => (
            <div className="timeline-row" key={`${time}-${title}`}>
              <time>{time}</time>
              <div>
                <strong>{title}</strong>
                <span>{detail}</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function PortfolioTable({ properties: scopedProperties }: { properties: typeof properties }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Property</th>
            <th>Type</th>
            <th>Units</th>
            <th>Occupancy</th>
            <th>Arrears</th>
            <th>NOI</th>
            <th>Service</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {scopedProperties.map((property) => (
            <tr key={property.id}>
              <td>
                <strong>{property.name}</strong>
                <span>{property.area}</span>
              </td>
              <td>{property.category}</td>
              <td>{property.units}</td>
              <td>
                <div className="cell-meter">
                  <b>{occupancy(property)}%</b>
                  <i style={{ width: `${occupancy(property)}%` }} />
                </div>
              </td>
              <td>{compactMoney(property.arrears)}</td>
              <td>{compactMoney(property.noi)}</td>
              <td>{property.serviceScore}</td>
              <td>
                <span className={`status ${statusTone(property.risk)}`}>{property.risk}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function PortfolioModule({ properties: scopedProperties }: { properties: typeof properties }) {
  return (
    <div className="portfolio-grid">
      {scopedProperties.map((property) => (
        <article className="property-card" key={property.id}>
          <div className="property-card-head">
            <div className="property-visual">
              <div />
              <span>{property.category.slice(0, 2)}</span>
            </div>
            <div>
              <p className="eyebrow">{property.area}</p>
              <h3>{property.name}</h3>
              <span>{property.address}</span>
            </div>
          </div>
          <div className="property-metrics">
            <Fact label="Manager" value={property.manager} />
            <Fact label="Unit Mix" value={property.mix} />
            <Fact label="Rent Roll" value={compactMoney(property.rentRoll)} />
            <Fact label="Deposit Held" value={compactMoney(property.deposits)} />
          </div>
          <div className="property-health">
            <Score label="Occupancy" value={occupancy(property)} />
            <Score label="Inspection" value={property.inspectionScore} />
            <Score label="Service" value={property.serviceScore} />
          </div>
          <div className="property-footer">
            <span className={`status ${statusTone(property.risk)}`}>{property.risk}</span>
            <small>{property.expiringLeases} renewal, {property.openTickets} ticket</small>
          </div>
        </article>
      ))}
    </div>
  );
}

function UnitsModule({ units: scopedUnits }: { units: typeof units; selectedPropertyId: string }) {
  const vacantCount = scopedUnits.filter((unit) => unit.status === 'Vacant').length;
  const delinquentCount = scopedUnits.filter((unit) => unit.status === 'Delinquent').length;

  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Unit Availability and Condition</h3>
            <p>Daftar unit dengan status tenant, kondisi, meter, dan aksi berikutnya.</p>
          </div>
          <button className="btn primary" type="button">
            + Add Unit
          </button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Unit</th>
                <th>Type</th>
                <th>Size</th>
                <th>Status</th>
                <th>Tenant</th>
                <th>Rent</th>
                <th>Lease End</th>
                <th>Condition</th>
                <th>Next Action</th>
              </tr>
            </thead>
            <tbody>
              {scopedUnits.map((unit) => (
                <tr key={unit.id}>
                  <td>
                    <strong>{unit.id}</strong>
                    <span>Floor {unit.floor}</span>
                  </td>
                  <td>{unit.type}</td>
                  <td>{unit.size} m2</td>
                  <td>
                    <span className={`status ${statusTone(unit.status)}`}>{unit.status}</span>
                  </td>
                  <td>{unit.tenant}</td>
                  <td>{compactMoney(unit.rent)}</td>
                  <td>{unit.leaseEnd}</td>
                  <td>
                    <strong>{unit.condition}</strong>
                    <span>{unit.meter}</span>
                  </td>
                  <td>{unit.nextAction}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <div className="panel-head compact">
          <h3>Make-Ready Board</h3>
        </div>
        <div className="stack-list">
          <Fact label="Vacant ready" value={`${vacantCount} unit`} />
          <Fact label="Delinquent watch" value={`${delinquentCount} unit`} />
          <Fact label="Avg make-ready" value="6.2 hari" />
          <Fact label="Listing gap" value="Rp 88Jt potential rent" />
        </div>
      </section>
    </div>
  );
}

function TenantsModule() {
  return (
    <div className="tenant-grid">
      {tenants.map((tenant) => (
        <article className="tenant-card" key={tenant.id}>
          <div className="tenant-head">
            <div>
              <p className="eyebrow">{tenant.id} / {tenant.segment}</p>
              <h3>{tenant.name}</h3>
              <span>{properties.find((property) => property.id === tenant.propertyId)?.name} / {tenant.unit}</span>
            </div>
            <span className={`status ${statusTone(tenant.status)}`}>{tenant.status}</span>
          </div>
          <div className="tenant-score">
            <div className="score-ring" style={{ '--score': tenant.health } as CSSProperties}>
              <strong>{tenant.health}</strong>
              <span>Health</span>
            </div>
            <div className="stack-list">
              <Fact label="Monthly Rent" value={compactMoney(tenant.rent)} />
              <Fact label="Balance" value={compactMoney(tenant.balance)} />
              <Fact label="Last Contact" value={tenant.lastContact} />
              <Fact label="Documents" value={tenant.documents} />
            </div>
          </div>
        </article>
      ))}
      <section className="panel tenant-log">
        <div className="panel-head compact">
          <h3>Communication Log</h3>
        </div>
        <div className="timeline">
          <div className="timeline-row">
            <time>Today</time>
            <div>
              <strong>Nadia Hartono</strong>
              <span>Minta renewal dengan pembayaran triwulanan.</span>
            </div>
          </div>
          <div className="timeline-row">
            <time>Fri</time>
            <div>
              <strong>Bima Santoso</strong>
              <span>Janji bayar Rp 20Jt sebelum 2 September 2026.</span>
            </div>
          </div>
          <div className="timeline-row">
            <time>Wed</time>
            <div>
              <strong>Kopi Lajur Selatan</strong>
              <span>Dokumen NIB baru masih menunggu tanda tangan direktur.</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function LeasesModule() {
  const stages = ['Active', 'Renewal Offered', 'Move Out Notice', 'Collection Hold'];

  return (
    <div className="pipeline-grid">
      {stages.map((stage) => (
        <section className="lane" key={stage}>
          <div className="lane-head">
            <h3>{stage}</h3>
            <span>{leases.filter((lease) => lease.stage === stage).length}</span>
          </div>
          {leases
            .filter((lease) => lease.stage === stage)
            .map((lease) => (
              <article className="lease-ticket" key={lease.id}>
                <p className="eyebrow">{lease.id} / {lease.unit}</p>
                <h4>{lease.tenant}</h4>
                <div className="ticket-facts">
                  <Fact label="Rent" value={compactMoney(lease.rent)} />
                  <Fact label="End" value={lease.end} />
                  <Fact label="Deposit" value={compactMoney(lease.deposit)} />
                  <Fact label="Escalation" value={lease.escalation} />
                </div>
                <div className="probability">
                  <span>Renewal probability</span>
                  <strong>{lease.probability}%</strong>
                  <div className="bar">
                    <i style={{ width: `${lease.probability}%` }} />
                  </div>
                </div>
                <small>{lease.action}</small>
              </article>
            ))}
        </section>
      ))}
    </div>
  );
}

function BillingModule({ invoices: scopedInvoices }: { invoices: typeof invoices }) {
  const collectable = scopedInvoices.reduce((sum, invoice) => sum + Math.max(invoice.amount - invoice.paid, 0), 0);

  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Accounts Receivable</h3>
            <p>Invoice, pembayaran parsial, aging, dan status follow-up.</p>
          </div>
          <button className="btn primary" type="button">
            + Create Invoice
          </button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Invoice</th>
                <th>Tenant</th>
                <th>Due</th>
                <th>Amount</th>
                <th>Paid</th>
                <th>Outstanding</th>
                <th>Aging</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {scopedInvoices.map((invoice) => (
                <tr key={invoice.id}>
                  <td>
                    <strong>{invoice.id}</strong>
                    <span>{properties.find((property) => property.id === invoice.propertyId)?.name}</span>
                  </td>
                  <td>{invoice.tenant}</td>
                  <td>{invoice.due}</td>
                  <td>{compactMoney(invoice.amount)}</td>
                  <td>{compactMoney(invoice.paid)}</td>
                  <td>{compactMoney(Math.max(invoice.amount - invoice.paid, 0))}</td>
                  <td>{invoice.aging}</td>
                  <td>
                    <span className={`status ${statusTone(invoice.status)}`}>{invoice.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <div className="panel-head compact">
          <h3>Collection Playbook</h3>
        </div>
        <div className="stack-list">
          <Fact label="Collectable" value={compactMoney(collectable)} />
          <Fact label="Reminder batch" value="14 tenant" />
          <Fact label="Payment plan" value="3 active" />
          <Fact label="Legal review" value="1 case" />
        </div>
      </section>
    </div>
  );
}

function MaintenanceModule({ orders }: { orders: typeof workOrders }) {
  const states = ['Vendor Assigned', 'Scheduled', 'Waiting Parts', 'In Progress', 'Diagnosing'];

  return (
    <div className="maintenance-board">
      {states.map((state) => (
        <section className="lane" key={state}>
          <div className="lane-head">
            <h3>{state}</h3>
            <span>{orders.filter((order) => order.state === state).length}</span>
          </div>
          {orders
            .filter((order) => order.state === state)
            .map((order) => (
              <article className="work-ticket" key={order.id}>
                <p className="eyebrow">{order.id} / {order.unit}</p>
                <h4>{order.title}</h4>
                <div className="ticket-facts">
                  <Fact label="Priority" value={order.priority} />
                  <Fact label="SLA" value={order.sla} />
                  <Fact label="Assignee" value={order.assignee} />
                  <Fact label="Cost" value={compactMoney(order.cost)} />
                </div>
              </article>
            ))}
        </section>
      ))}
    </div>
  );
}

function InspectionModule() {
  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Inspection Calendar</h3>
            <p>Prioritas pemeriksaan berdasarkan due date, score, dan jumlah finding.</p>
          </div>
          <button className="btn primary" type="button">
            + Schedule
          </button>
        </div>
        <div className="inspection-list">
          {inspections.map((inspection) => (
            <div className="inspection-row" key={inspection.id}>
              <div className="score-ring small" style={{ '--score': inspection.score } as CSSProperties}>
                <strong>{inspection.score}</strong>
              </div>
              <div>
                <p className="eyebrow">{inspection.id} / {inspection.due}</p>
                <h3>{inspection.scope}</h3>
                <span>{properties.find((property) => property.id === inspection.propertyId)?.name}</span>
              </div>
              <span className={`status ${statusTone(inspection.status)}`}>{inspection.status}</span>
              <strong>{inspection.findings} findings</strong>
            </div>
          ))}
        </div>
      </section>
      <section className="panel">
        <div className="panel-head compact">
          <h3>Compliance Snapshot</h3>
        </div>
        <div className="checklist">
          {['Fire certificate', 'Lift permit', 'PBB archive', 'Insurance policy', 'Tenant KYC'].map((item, index) => (
            <label key={item}>
              <input type="checkbox" defaultChecked={index < 3} />
              <span>{item}</span>
            </label>
          ))}
        </div>
      </section>
    </div>
  );
}

function DocumentsModule() {
  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Document Vault</h3>
            <p>Kontrol dokumen legal, compliance, handover, dan asset ownership.</p>
          </div>
          <button className="btn primary" type="button">
            + Upload
          </button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Document</th>
                <th>Entity</th>
                <th>Type</th>
                <th>Owner</th>
                <th>Expiry</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((document) => (
                <tr key={document.id}>
                  <td>
                    <strong>{document.name}</strong>
                    <span>{document.id}</span>
                  </td>
                  <td>{document.entity}</td>
                  <td>{document.type}</td>
                  <td>{document.owner}</td>
                  <td>{document.expiry}</td>
                  <td>
                    <span className={`status ${statusTone(document.status)}`}>{document.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <div className="panel-head compact">
          <h3>Missing Evidence</h3>
        </div>
        <div className="stack-list">
          <Fact label="Tenant KYC" value="2 pending" />
          <Fact label="BAST photo" value="1 draft" />
          <Fact label="Insurance renewal" value="BSD review" />
          <Fact label="Tax profile" value="1 NIB pending" />
        </div>
      </section>
    </div>
  );
}

function ReportsModule() {
  return (
    <div className="report-grid">
      {reportPacks.map(([title, detail]) => (
        <article className="report-card" key={title}>
          <div className="report-icon">{title.slice(0, 2)}</div>
          <h3>{title}</h3>
          <p>{detail}</p>
          <button className="btn secondary" type="button">
            Generate
          </button>
        </article>
      ))}
    </div>
  );
}

function SettingsModule() {
  return (
    <div className="dashboard-grid">
      <section className="panel wide">
        <div className="panel-head">
          <div>
            <h3>Role and Approval Matrix</h3>
            <p>Akses dibuat berdasarkan pekerjaan nyata property manager, finance, facility, dan owner.</p>
          </div>
          <button className="btn primary" type="button">
            + Invite User
          </button>
        </div>
        <div className="role-grid">
          {roles.map(([title, detail]) => (
            <article className="role-row" key={title}>
              <strong>{title}</strong>
              <span>{detail}</span>
            </article>
          ))}
        </div>
      </section>
      <section className="panel">
        <div className="panel-head compact">
          <h3>Business Rules</h3>
        </div>
        <div className="checklist">
          <label>
            <input type="checkbox" defaultChecked />
            <span>Auto-generate invoice H-7</span>
          </label>
          <label>
            <input type="checkbox" defaultChecked />
            <span>Require photo before WO close</span>
          </label>
          <label>
            <input type="checkbox" defaultChecked />
            <span>Owner approval for capex</span>
          </label>
          <label>
            <input type="checkbox" />
            <span>Lock lease after e-sign</span>
          </label>
        </div>
      </section>
    </div>
  );
}

function WorkOrderRow({ order }: { order: (typeof workOrders)[number] }) {
  return (
    <div className="work-item">
      <div>
        <strong>{order.id}</strong>
        <span>{order.title}</span>
      </div>
      <small>{order.priority} / {order.sla}</small>
    </div>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div className="fact">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Score({ label, value }: { label: string; value: number }) {
  return (
    <div className="score">
      <div className="bar">
        <i style={{ width: `${value}%` }} />
      </div>
      <span>{label}</span>
      <strong>{value}%</strong>
    </div>
  );
}
