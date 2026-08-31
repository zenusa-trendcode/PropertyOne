from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from pms.models import (
    ActivityEvent,
    ApprovalRequest,
    Document,
    Inspection,
    InspectionFinding,
    Invoice,
    Lease,
    Organization,
    Payment,
    Property,
    Tenant,
    Unit,
    Vendor,
    WorkOrder,
)


def d(value: str) -> Decimal:
    return Decimal(value)


class Command(BaseCommand):
    help = 'Seed realistic PMS demo data and a demo admin user.'

    def handle(self, *args, **options):
        User = get_user_model()
        admin, _ = User.objects.update_or_create(
            username='admin',
            defaults={
                'email': 'admin@propertione.local',
                'first_name': 'Artha',
                'last_name': 'Ops',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        admin.set_password('Admin12345!')
        admin.save(update_fields=['password', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active'])

        org, _ = Organization.objects.update_or_create(
            name='Artha Property Management',
            defaults={
                'legal_name': 'PT Artha Properti Nusantara',
                'tax_id': '09.812.991.4-012.000',
                'default_currency': 'IDR',
                'email': 'finance@propertione.local',
                'phone': '+62 21 5010 8800',
                'address': 'Revenue Tower, Jakarta Selatan',
            },
        )

        properties = {}
        property_rows = [
            ('KMG', 'Artha Residence Kemang', Property.Type.APARTMENT, Property.Status.STABILIZED, 'Jl. Kemang Raya 18', 'Jakarta Selatan', 'DKI Jakarta', 'Maya Putri', 'maya@propertione.local', '18250', '14200', '28500', '8000', 7),
            ('BSD', 'Nusa Office Park', Property.Type.OFFICE, Property.Status.WATCHLIST, 'Green Office Boulevard Kav. 6', 'BSD City', 'Banten', 'Rizky Pratama', 'rizky@propertione.local', '28800', '22600', '42000', '12000', 10),
            ('SPG', 'Serpong Garden Cluster', Property.Type.TOWNHOUSE, Property.Status.LEASE_UP, 'Cluster Gardenia Blok A', 'Tangerang Selatan', 'Banten', 'Dewi Lestari', 'dewi@propertione.local', '9800', '8700', '18500', '6500', 5),
            ('CGU', 'Canggu Living Suites', Property.Type.VILLA, Property.Status.ACTIVE, 'Jl. Pantai Batu Bolong 42', 'Badung', 'Bali', 'Made Ari', 'made@propertione.local', '6400', '5150', '55000', '15000', 8),
        ]
        for code, name, ptype, status, address, city, province, manager, email, gross, nla, svc, sinking, statement_day in property_rows:
            properties[code], _ = Property.objects.update_or_create(
                property_code=code,
                defaults={
                    'organization': org,
                    'name': name,
                    'property_type': ptype,
                    'status': status,
                    'address': address,
                    'city': city,
                    'province': province,
                    'manager_name': manager,
                    'manager_email': email,
                    'gross_area_sqm': d(gross),
                    'net_leasable_area_sqm': d(nla),
                    'service_charge_rate': d(svc),
                    'sinking_fund_rate': d(sinking),
                    'owner_statement_day': statement_day,
                },
            )

        unit_rows = [
            ('KMG', 'A-1207', '12', Unit.Type.TWO_BR, '72', 2, 2, Unit.Status.OCCUPIED, '19000000', '18500000', 'Good', 'PLN-771202', 'Renewal call'),
            ('KMG', 'B-0811', '08', Unit.Type.STUDIO, '32', 0, 1, Unit.Status.NOTICE, '9000000', '8700000', 'Need paint', 'PLN-771811', 'Schedule handover'),
            ('KMG', 'C-0302', '03', Unit.Type.ONE_BR, '48', 1, 1, Unit.Status.MAKE_READY, '12500000', '0', 'Deep cleaning', 'PLN-770302', 'Vendor cleaning'),
            ('BSD', 'R-03', 'GF', Unit.Type.RETAIL, '110', 0, 1, Unit.Status.OCCUPIED, '55000000', '52000000', 'Good', 'PLN-880003', 'VAT document'),
            ('BSD', 'O-1702', '17', Unit.Type.OFFICE, '240', 0, 2, Unit.Status.VACANT, '88000000', '0', 'Ready', 'PLN-881702', 'Publish listing'),
            ('BSD', 'S-12', 'B1', Unit.Type.STORAGE, '60', 0, 0, Unit.Status.OCCUPIED, '14500000', '13500000', 'Good', 'PLN-880112', 'Access card audit'),
            ('SPG', 'G-12', 'Cluster', Unit.Type.THREE_BR, '138', 3, 3, Unit.Status.DELINQUENT, '16500000', '15500000', 'Minor leak', 'PLN-660012', 'Payment plan'),
            ('SPG', 'G-18', 'Cluster', Unit.Type.TWO_BR, '102', 2, 2, Unit.Status.VACANT, '12800000', '0', 'Ready', 'PLN-660018', 'Open house'),
            ('CGU', 'V-09', 'Villa', Unit.Type.VILLA, '95', 1, 1, Unit.Status.OCCUPIED, '45000000', '42000000', 'Excellent', 'PLN-990009', 'Guest compliance'),
        ]
        units = {}
        for pcode, unit_code, floor, utype, area, beds, baths, status, market, current, handover, meter, action in unit_rows:
            units[unit_code], _ = Unit.objects.update_or_create(
                property=properties[pcode],
                unit_code=unit_code,
                defaults={
                    'floor': floor,
                    'unit_type': utype,
                    'area_sqm': d(area),
                    'bedrooms': beds,
                    'bathrooms': baths,
                    'status': status,
                    'market_rent': d(market),
                    'current_rent': d(current),
                    'handover_state': handover,
                    'meter_electric': meter,
                    'meter_water': f'PDAM-{unit_code}',
                    'next_action': action,
                },
            )

        tenant_rows = [
            ('T-1001', Tenant.Type.INDIVIDUAL, 'Nadia Hartono', 'Nadia Hartono', '3275015501890001', 'nadia@example.com', '+62 812 1100 1207', Tenant.Risk.EXCELLENT, Tenant.KycStatus.COMPLETE, 96, date(2026, 8, 28), 'Prefers quarterly payment reminder.'),
            ('T-1002', Tenant.Type.COMPANY, 'Kopi Lajur Selatan', 'PT Kopi Lajur Selatan', '74.102.991.3-411.000', 'finance@kopilajur.test', '+62 21 8080 1203', Tenant.Risk.MONITOR, Tenant.KycStatus.PARTIAL, 82, date(2026, 8, 25), 'NIB update pending.'),
            ('T-1003', Tenant.Type.INDIVIDUAL, 'Bima Santoso', 'Bima Santoso', '3674081402850002', 'bima@example.com', '+62 813 9000 0012', Tenant.Risk.AT_RISK, Tenant.KycStatus.COMPLETE, 58, date(2026, 8, 21), 'Payment commitment required before September.'),
            ('T-1004', Tenant.Type.COMPANY, 'Oceanlane Studio', 'PT Oceanlane Studio Kreatif', '88.450.991.1-908.000', 'ops@oceanlane.test', '+62 361 778 909', Tenant.Risk.EXCELLENT, Tenant.KycStatus.COMPLETE, 91, date(2026, 8, 26), 'Long-stay guest usage audit every quarter.'),
            ('T-1005', Tenant.Type.COMPANY, 'Metro Archive Services', 'PT Metro Arsip Indonesia', '31.120.771.6-331.000', 'billing@metroarchive.test', '+62 21 5599 1221', Tenant.Risk.EXCELLENT, Tenant.KycStatus.COMPLETE, 88, date(2026, 8, 20), 'Requires PO number on invoice.'),
        ]
        tenants = {}
        for code, ttype, display, legal, tax, email, phone, risk, kyc, health, contact, notes in tenant_rows:
            tenants[code], _ = Tenant.objects.update_or_create(
                tenant_code=code,
                defaults={
                    'organization': org,
                    'tenant_type': ttype,
                    'display_name': display,
                    'legal_name': legal,
                    'tax_id': tax,
                    'email': email,
                    'phone': phone,
                    'billing_address': 'Same as leased unit',
                    'risk_level': risk,
                    'kyc_status': kyc,
                    'tenant_health_score': health,
                    'last_contact_date': contact,
                    'notes': notes,
                },
            )

        leases = {}
        lease_rows = [
            ('LS-24031', 'T-1001', 'KMG', 'A-1207', Lease.Status.RENEWAL, date(2025, 11, 1), date(2026, 10, 31), '18500000', '37000000', '2500000', Lease.BillingCycle.MONTHLY, '5% annual', '5', 72, 'Negotiate 2-year term.'),
            ('LS-24028', 'T-1004', 'KMG', 'B-0811', Lease.Status.NOTICE, date(2025, 9, 19), date(2026, 9, 18), '8700000', '17400000', '950000', Lease.BillingCycle.MONTHLY, 'Fixed', '0', 18, 'Prepare make-ready after move-out.'),
            ('LS-23012', 'T-1002', 'BSD', 'R-03', Lease.Status.ACTIVE, date(2024, 3, 1), date(2027, 2, 28), '52000000', '156000000', '9400000', Lease.BillingCycle.MONTHLY, 'CPI capped 8%', '6', 88, 'Collect updated NIB.'),
            ('LS-25004', 'T-1003', 'SPG', 'G-12', Lease.Status.COLLECTION, date(2025, 12, 16), date(2026, 12, 15), '15500000', '31000000', '0', Lease.BillingCycle.MONTHLY, '5% annual', '5', 42, 'Payment commitment required.'),
            ('LS-25017', 'T-1004', 'CGU', 'V-09', Lease.Status.ACTIVE, date(2026, 5, 1), date(2027, 4, 30), '42000000', '84000000', '4800000', Lease.BillingCycle.MONTHLY, '6% annual', '6', 91, 'Guest usage audit.'),
            ('LS-24107', 'T-1005', 'BSD', 'S-12', Lease.Status.ACTIVE, date(2025, 1, 1), date(2026, 12, 31), '13500000', '27000000', '2100000', Lease.BillingCycle.MONTHLY, 'Fixed', '0', 79, 'Renewal discussion in October.'),
        ]
        for code, tcode, pcode, ucode, status, start, end, rent, deposit, service, cycle, esc_type, esc_rate, probability, notes in lease_rows:
            leases[code], _ = Lease.objects.update_or_create(
                lease_code=code,
                defaults={
                    'tenant': tenants[tcode],
                    'property': properties[pcode],
                    'unit': units[ucode],
                    'status': status,
                    'start_date': start,
                    'end_date': end,
                    'rent_amount': d(rent),
                    'deposit_amount': d(deposit),
                    'service_charge_amount': d(service),
                    'billing_cycle': cycle,
                    'escalation_type': esc_type,
                    'escalation_rate': d(esc_rate),
                    'renewal_probability': probability,
                    'notes': notes,
                },
            )

        invoice_rows = [
            ('INV-0826-001', 'T-1002', 'BSD', 'LS-23012', Invoice.LineType.RENT, Invoice.Status.PARTIAL, date(2026, 8, 1), date(2026, 8, 15), '52000000', '5720000', '0', '40000000', 2),
            ('INV-0826-008', 'T-1003', 'SPG', 'LS-25004', Invoice.LineType.RENT, Invoice.Status.OVERDUE, date(2026, 8, 1), date(2026, 7, 31), '15500000', '0', '0', '0', 3),
            ('INV-0726-044', 'T-1003', 'SPG', 'LS-25004', Invoice.LineType.RENT, Invoice.Status.ESCALATED, date(2026, 7, 1), date(2026, 7, 1), '15500000', '0', '0', '0', 5),
            ('INV-0826-011', 'T-1001', 'KMG', 'LS-24031', Invoice.LineType.RENT, Invoice.Status.PAID, date(2026, 8, 1), date(2026, 8, 10), '18500000', '0', '0', '18500000', 0),
            ('INV-0826-020', 'T-1004', 'CGU', 'LS-25017', Invoice.LineType.RENT, Invoice.Status.PAID, date(2026, 8, 1), date(2026, 8, 20), '42000000', '4620000', '0', '46620000', 0),
            ('INV-0826-027', 'T-1005', 'BSD', 'LS-24107', Invoice.LineType.SERVICE, Invoice.Status.ISSUED, date(2026, 8, 5), date(2026, 9, 5), '2100000', '231000', '0', '0', 0),
        ]
        invoices = {}
        for number, tcode, pcode, lcode, line_type, status, issue, due, subtotal, tax, discount, paid, reminders in invoice_rows:
            invoices[number], _ = Invoice.objects.update_or_create(
                invoice_number=number,
                defaults={
                    'tenant': tenants[tcode],
                    'property': properties[pcode],
                    'lease': leases[lcode],
                    'line_type': line_type,
                    'status': status,
                    'issue_date': issue,
                    'due_date': due,
                    'subtotal': d(subtotal),
                    'tax': d(tax),
                    'discount': d(discount),
                    'paid_amount': d(paid),
                    'reminder_count': reminders,
                    'notes': 'Generated by demo seed.',
                },
            )

        payment_rows = [
            ('PAY-BCA-8821', 'INV-0826-011', date(2026, 8, 8), '18500000', Payment.Method.BANK_TRANSFER),
            ('PAY-MDR-9201', 'INV-0826-001', date(2026, 8, 18), '40000000', Payment.Method.VIRTUAL_ACCOUNT),
            ('PAY-BNI-7781', 'INV-0826-020', date(2026, 8, 20), '46620000', Payment.Method.BANK_TRANSFER),
        ]
        for reference, invoice_number, payment_date, amount, method in payment_rows:
            Payment.objects.update_or_create(
                reference=reference,
                defaults={
                    'invoice': invoices[invoice_number],
                    'payment_date': payment_date,
                    'amount': d(amount),
                    'method': method,
                    'matched_by': 'Auto matcher',
                },
            )

        vendors = {}
        vendor_rows = [
            ('V-HVAC-01', 'CoolPro HVAC', Vendor.Category.HVAC, 'Andi Saputra', '+62 812 9000 7711', 'ops@coolpro.test', 6, '4.70'),
            ('V-LIFT-01', 'Kone Service Partner', Vendor.Category.GENERAL, 'Nina Wijaya', '+62 21 5599 8877', 'dispatch@konepartner.test', 24, '4.55'),
            ('V-MEP-01', 'Prima MEP Facility', Vendor.Category.ELECTRICAL, 'Reno Aditya', '+62 812 8811 2200', 'service@primamep.test', 12, '4.30'),
            ('V-ROOF-01', 'Baja Roof Solution', Vendor.Category.GENERAL, 'Agus Rinaldi', '+62 813 7722 1300', 'team@bajaroof.test', 18, '4.10'),
        ]
        for code, name, category, contact, phone, email, sla, rating in vendor_rows:
            vendors[code], _ = Vendor.objects.update_or_create(
                vendor_code=code,
                defaults={
                    'name': name,
                    'category': category,
                    'contact_person': contact,
                    'phone': phone,
                    'email': email,
                    'sla_hours': sla,
                    'rating': d(rating),
                    'is_active': True,
                },
            )

        now = timezone.now()
        work_rows = [
            ('WO-1048', 'KMG', 'A-1207', 'T-1001', 'V-HVAC-01', 'AC bocor unit A-1207', 'Drain pan overflow, tenant requests same-day visit.', WorkOrder.Priority.EMERGENCY, WorkOrder.Category.HVAC, WorkOrder.Status.ASSIGNED, now - timedelta(hours=3), now + timedelta(hours=5), 'Nadia Hartono', '1250000', '2000000', '0', False),
            ('WO-1047', 'KMG', None, None, 'V-LIFT-01', 'Lift tower A inspeksi bulanan', 'Preventive maintenance and safety certificate check.', WorkOrder.Priority.PREVENTIVE, WorkOrder.Category.OTHER, WorkOrder.Status.ASSIGNED, now - timedelta(days=1), now + timedelta(days=2), 'Facility Lead', '0', '0', '0', False),
            ('WO-1045', 'BSD', None, None, 'V-MEP-01', 'Pompa transfer basement', 'Pump vibration over threshold and needs bearing replacement.', WorkOrder.Priority.HIGH, WorkOrder.Category.PLUMBING, WorkOrder.Status.PARTS, now - timedelta(hours=18), now + timedelta(hours=12), 'Security Desk', '8700000', '9000000', '0', True),
            ('WO-1043', 'KMG', None, None, None, 'Cat ulang koridor lantai 9', 'Paint touch-up after tenant move-in works.', WorkOrder.Priority.MEDIUM, WorkOrder.Category.OTHER, WorkOrder.Status.IN_PROGRESS, now - timedelta(days=2), now + timedelta(days=5), 'Property Admin', '3400000', '3500000', '0', False),
            ('WO-1039', 'SPG', 'G-12', 'T-1003', 'V-ROOF-01', 'Kebocoran dak carport', 'Water intrusion after heavy rain.', WorkOrder.Priority.HIGH, WorkOrder.Category.STRUCTURAL, WorkOrder.Status.TRIAGED, now - timedelta(hours=14), now + timedelta(hours=18), 'Bima Santoso', '0', '0', '0', False),
        ]
        for number, pcode, ucode, tcode, vcode, title, description, priority, category, status, reported, due, requester, estimate, budget, actual, approval in work_rows:
            WorkOrder.objects.update_or_create(
                work_order_number=number,
                defaults={
                    'property': properties[pcode],
                    'unit': units.get(ucode) if ucode else None,
                    'tenant': tenants.get(tcode) if tcode else None,
                    'vendor': vendors.get(vcode) if vcode else None,
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'category': category,
                    'status': status,
                    'reported_at': reported,
                    'due_at': due,
                    'requester': requester,
                    'estimated_cost': d(estimate),
                    'approved_budget': d(budget),
                    'actual_cost': d(actual),
                    'requires_owner_approval': approval,
                    'before_photo_required': True,
                    'after_photo_required': True,
                },
            )

        inspection_rows = [
            ('INSP-081', 'KMG', None, 'Fire safety and hydrant', Inspection.Status.SCHEDULED, date(2026, 9, 3), None, 'Raka HSE', 92, 'Hydrant pressure within threshold.'),
            ('INSP-076', 'BSD', None, 'Retail signage compliance', Inspection.Status.NEEDS_ACTION, date(2026, 9, 5), None, 'Sari Compliance', 78, 'Several retail tenants use unapproved signage.'),
            ('INSP-072', 'SPG', 'G-12', 'Roof and gutter survey', Inspection.Status.CRITICAL, date(2026, 8, 31), None, 'Prima Surveyor', 69, 'Immediate roof remediation required.'),
            ('INSP-067', 'CGU', 'V-09', 'Guest safety checklist', Inspection.Status.COMPLETE, date(2026, 8, 25), date(2026, 8, 25), 'Made Ari', 96, 'Ready for long-stay guest.'),
        ]
        inspections = {}
        for number, pcode, ucode, scope, status, scheduled, completed, inspector, score, notes in inspection_rows:
            inspections[number], _ = Inspection.objects.update_or_create(
                inspection_number=number,
                defaults={
                    'property': properties[pcode],
                    'unit': units.get(ucode) if ucode else None,
                    'scope': scope,
                    'status': status,
                    'scheduled_date': scheduled,
                    'completed_date': completed,
                    'inspector': inspector,
                    'score': score,
                    'notes': notes,
                },
            )

        finding_rows = [
            ('INSP-076', 'Unapproved illuminated signage', InspectionFinding.Severity.MEDIUM, 'Send notice and require design approval.', InspectionFinding.Status.ASSIGNED, date(2026, 9, 12)),
            ('INSP-072', 'Gutter slope causing pooling', InspectionFinding.Severity.CRITICAL, 'Assign roof vendor and document before/after photos.', InspectionFinding.Status.OPEN, date(2026, 9, 2)),
            ('INSP-081', 'Extinguisher tag near expiry', InspectionFinding.Severity.LOW, 'Replace tag during scheduled HSE round.', InspectionFinding.Status.OPEN, date(2026, 9, 10)),
        ]
        for insp_number, title, severity, action, status, due_date in finding_rows:
            InspectionFinding.objects.update_or_create(
                inspection=inspections[insp_number],
                title=title,
                defaults={
                    'severity': severity,
                    'corrective_action': action,
                    'status': status,
                    'due_date': due_date,
                },
            )

        document_rows = [
            ('DOC-221', 'Lease agreement signed', Document.Type.LEASE, Document.Status.COMPLETE, 'Legal Ops', date(2026, 10, 31), 'KMG', 'T-1001', 'LS-24031'),
            ('DOC-219', 'Tenant NIB and tax profile', Document.Type.KYC, Document.Status.PENDING, 'Account Manager', date(2026, 9, 7), 'BSD', 'T-1002', 'LS-23012'),
            ('DOC-211', 'BAST move-out checklist', Document.Type.HANDOVER, Document.Status.DRAFT, 'Property Admin', date(2026, 9, 18), 'KMG', 'T-1004', 'LS-24028'),
            ('DOC-204', 'Insurance building policy', Document.Type.INSURANCE, Document.Status.REVIEW, 'Finance', date(2026, 12, 1), 'BSD', None, None),
            ('DOC-199', 'PBB archive 2026', Document.Type.TAX, Document.Status.COMPLETE, 'Finance', date(2027, 3, 31), 'SPG', None, None),
        ]
        for number, title, dtype, status, owner, expiry, pcode, tcode, lcode in document_rows:
            Document.objects.update_or_create(
                document_number=number,
                defaults={
                    'title': title,
                    'document_type': dtype,
                    'status': status,
                    'owner': owner,
                    'expiry_date': expiry,
                    'property': properties.get(pcode),
                    'tenant': tenants.get(tcode) if tcode else None,
                    'lease': leases.get(lcode) if lcode else None,
                    'notes': 'Document metadata seeded for demo vault.',
                },
            )

        approval_rows = [
            ('APR-089', 'BSD', 'WorkOrder', 'WO-1045', 'Approve pump bearing replacement', 'Rizky Pratama', 'Owner Rep', '9000000', ApprovalRequest.Status.PENDING, date(2026, 8, 31)),
            ('APR-088', 'SPG', 'Collection', 'INV-0726-044', 'Approve legal collection notice', 'Dewi Lestari', 'Legal Ops', '15500000', ApprovalRequest.Status.PENDING, date(2026, 9, 1)),
            ('APR-084', 'KMG', 'Lease', 'LS-24031', 'Approve renewal discount 3%', 'Maya Putri', 'Finance Director', '6660000', ApprovalRequest.Status.APPROVED, date(2026, 8, 22)),
        ]
        for number, pcode, object_type, ref, title, requested_by, approver, amount, status, due_date in approval_rows:
            ApprovalRequest.objects.update_or_create(
                request_number=number,
                defaults={
                    'property': properties[pcode],
                    'object_type': object_type,
                    'object_reference': ref,
                    'title': title,
                    'requested_by': requested_by,
                    'approver_name': approver,
                    'amount': d(amount),
                    'status': status,
                    'due_date': due_date,
                    'decision_note': '',
                },
            )

        ActivityEvent.objects.all().delete()
        activity_rows = [
            ('PAYMENT', 'Payment received', 'Oceanlane Studio membayar invoice Agustus penuh.', 'CGU', 'Auto matcher', now - timedelta(hours=1)),
            ('WORK_ORDER', 'Work order escalated', 'WO-1048 butuh vendor HVAC hari ini.', 'KMG', 'Maya Putri', now - timedelta(hours=2)),
            ('LEASE', 'Lease renewal', 'Nadia Hartono meminta opsi kontrak 24 bulan.', 'KMG', 'Maya Putri', now - timedelta(hours=3)),
            ('INSPECTION', 'Inspection alert', 'Serpong Garden roof survey berada di bawah ambang skor.', 'SPG', 'Dewi Lestari', now - timedelta(hours=5)),
            ('DOCUMENT', 'KYC document pending', 'Kopi Lajur Selatan belum menyerahkan NIB terbaru.', 'BSD', 'Rizky Pratama', now - timedelta(hours=7)),
        ]
        for event_type, title, description, pcode, actor, event_time in activity_rows:
            ActivityEvent.objects.create(
                event_type=getattr(ActivityEvent.Type, event_type),
                title=title,
                description=description,
                property=properties[pcode],
                actor=actor,
                event_time=event_time,
            )

        self.stdout.write(self.style.SUCCESS('Demo PMS data seeded. Login with admin / Admin12345!'))
