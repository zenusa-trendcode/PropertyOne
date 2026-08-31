from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from .forms import (
    ApprovalRequestForm,
    DocumentForm,
    InspectionForm,
    InvoiceForm,
    LeaseForm,
    OrganizationForm,
    PropertyForm,
    TenantForm,
    UnitForm,
    VendorForm,
    WorkOrderForm,
)
from .models import (
    ActivityEvent,
    ApprovalRequest,
    Document,
    Inspection,
    Invoice,
    Lease,
    Organization,
    Property,
    Tenant,
    Unit,
    Vendor,
    WorkOrder,
)


@dataclass(frozen=True)
class ModuleSpec:
    slug: str
    title: str
    subtitle: str
    group: str
    code: str
    model: type
    form: type
    columns: tuple[tuple[str, str, str], ...]
    detail_fields: tuple[tuple[str, str, str], ...]
    search_fields: tuple[str, ...]
    order_by: tuple[str, ...]
    property_filter: str | None = None


def money(value: Decimal | int | float | None) -> str:
    if value is None:
        return '-'
    decimal = Decimal(value)
    return f'Rp {decimal:,.0f}'.replace(',', '.')


def percent(value: Any) -> str:
    if value in [None, '']:
        return '-'
    return f'{value}%'


def status_tone(value: Any) -> str:
    text = str(value).lower()
    if any(token in text for token in ['risk', 'critical', 'overdue', 'escalated', 'delinquent', 'collection', 'approval']):
        return 'danger'
    if any(token in text for token in ['pending', 'partial', 'notice', 'review', 'monitor', 'watch', 'parts', 'draft']):
        return 'warning'
    if any(token in text for token in ['active', 'paid', 'complete', 'excellent', 'stabil', 'closed', 'assigned', 'scheduled']):
        return 'success'
    return 'neutral'


def resolve_attr(obj: Any, path: str) -> Any:
    current = obj
    for part in path.split('__'):
        current = getattr(current, part)
        if callable(current):
            current = current()
        if current is None:
            return None
    return current


def display_value(obj: Any, path: str, kind: str = 'text') -> str:
    value = resolve_attr(obj, path)
    if kind == 'money':
        return money(value)
    if kind == 'percent':
        return percent(value)
    if kind == 'date' and value:
        return value.strftime('%d %b %Y')
    if kind == 'datetime' and value:
        return timezone.localtime(value).strftime('%d %b %Y %H:%M')
    if kind == 'bool':
        return 'Yes' if value else 'No'
    return str(value) if value not in [None, ''] else '-'


MODULES: dict[str, ModuleSpec] = {
    'organizations': ModuleSpec(
        slug='organizations',
        title='Organizations',
        subtitle='Owner company, operating entity, currency, tax profile, and contact context.',
        group='Control',
        code='OR',
        model=Organization,
        form=OrganizationForm,
        columns=(
            ('Name', 'name', 'text'),
            ('Legal Name', 'legal_name', 'text'),
            ('Currency', 'default_currency', 'text'),
            ('Email', 'email', 'text'),
            ('Phone', 'phone', 'text'),
        ),
        detail_fields=(
            ('Name', 'name', 'text'),
            ('Legal Name', 'legal_name', 'text'),
            ('Tax ID', 'tax_id', 'text'),
            ('Currency', 'default_currency', 'text'),
            ('Email', 'email', 'text'),
            ('Phone', 'phone', 'text'),
            ('Address', 'address', 'text'),
        ),
        search_fields=('name', 'legal_name', 'tax_id', 'email'),
        order_by=('name',),
    ),
    'properties': ModuleSpec(
        slug='properties',
        title='Properties',
        subtitle='Portfolio master data, ownership context, service charge settings, and operational ownership.',
        group='Operations',
        code='PF',
        model=Property,
        form=PropertyForm,
        columns=(
            ('Property', 'name', 'text'),
            ('Code', 'property_code', 'text'),
            ('Type', 'get_property_type_display', 'text'),
            ('City', 'city', 'text'),
            ('Manager', 'manager_name', 'text'),
            ('Occupancy', 'occupancy_rate', 'percent'),
            ('Rent Roll', 'active_rent_roll', 'money'),
            ('Status', 'get_status_display', 'status'),
        ),
        detail_fields=(
            ('Property Code', 'property_code', 'text'),
            ('Name', 'name', 'text'),
            ('Organization', 'organization', 'text'),
            ('Type', 'get_property_type_display', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Address', 'address', 'text'),
            ('City', 'city', 'text'),
            ('Manager', 'manager_name', 'text'),
            ('Manager Email', 'manager_email', 'text'),
            ('Gross Area', 'gross_area_sqm', 'text'),
            ('Net Leasable Area', 'net_leasable_area_sqm', 'text'),
            ('Service Charge Rate', 'service_charge_rate', 'money'),
            ('Sinking Fund Rate', 'sinking_fund_rate', 'money'),
            ('Owner Statement Day', 'owner_statement_day', 'text'),
        ),
        search_fields=('name', 'property_code', 'city', 'manager_name'),
        order_by=('name',),
    ),
    'units': ModuleSpec(
        slug='units',
        title='Units',
        subtitle='Availability, current rent, market rent, handover state, utility meter, and next action per unit.',
        group='Operations',
        code='UN',
        model=Unit,
        form=UnitForm,
        columns=(
            ('Unit', 'unit_code', 'text'),
            ('Property', 'property__name', 'text'),
            ('Type', 'get_unit_type_display', 'text'),
            ('Area', 'area_sqm', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Market Rent', 'market_rent', 'money'),
            ('Current Rent', 'current_rent', 'money'),
            ('Next Action', 'next_action', 'text'),
        ),
        detail_fields=(
            ('Property', 'property__name', 'text'),
            ('Unit Code', 'unit_code', 'text'),
            ('Floor', 'floor', 'text'),
            ('Type', 'get_unit_type_display', 'text'),
            ('Area', 'area_sqm', 'text'),
            ('Bedrooms', 'bedrooms', 'text'),
            ('Bathrooms', 'bathrooms', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Market Rent', 'market_rent', 'money'),
            ('Current Rent', 'current_rent', 'money'),
            ('Handover State', 'handover_state', 'text'),
            ('Electric Meter', 'meter_electric', 'text'),
            ('Water Meter', 'meter_water', 'text'),
            ('Next Action', 'next_action', 'text'),
        ),
        search_fields=('unit_code', 'property__name', 'handover_state', 'next_action'),
        order_by=('property__name', 'unit_code'),
        property_filter='property_id',
    ),
    'tenants': ModuleSpec(
        slug='tenants',
        title='Tenants',
        subtitle='Tenant identity, KYC, risk score, contact history, and collection exposure.',
        group='Operations',
        code='TN',
        model=Tenant,
        form=TenantForm,
        columns=(
            ('Tenant', 'display_name', 'text'),
            ('Code', 'tenant_code', 'text'),
            ('Type', 'get_tenant_type_display', 'text'),
            ('Risk', 'get_risk_level_display', 'status'),
            ('KYC', 'get_kyc_status_display', 'status'),
            ('Health', 'tenant_health_score', 'percent'),
            ('Balance', 'outstanding_balance', 'money'),
            ('Last Contact', 'last_contact_date', 'date'),
        ),
        detail_fields=(
            ('Tenant Code', 'tenant_code', 'text'),
            ('Display Name', 'display_name', 'text'),
            ('Legal Name', 'legal_name', 'text'),
            ('Type', 'get_tenant_type_display', 'text'),
            ('Tax ID', 'tax_id', 'text'),
            ('Email', 'email', 'text'),
            ('Phone', 'phone', 'text'),
            ('Risk', 'get_risk_level_display', 'status'),
            ('KYC', 'get_kyc_status_display', 'status'),
            ('Health Score', 'tenant_health_score', 'percent'),
            ('Outstanding Balance', 'outstanding_balance', 'money'),
            ('Last Contact', 'last_contact_date', 'date'),
            ('Billing Address', 'billing_address', 'text'),
            ('Notes', 'notes', 'text'),
        ),
        search_fields=('display_name', 'tenant_code', 'legal_name', 'tax_id', 'email', 'phone'),
        order_by=('display_name',),
    ),
    'leases': ModuleSpec(
        slug='leases',
        title='Leases',
        subtitle='Lease lifecycle, rent, deposit, billing cycle, renewal probability, and escalation terms.',
        group='Operations',
        code='LS',
        model=Lease,
        form=LeaseForm,
        columns=(
            ('Lease', 'lease_code', 'text'),
            ('Tenant', 'tenant__display_name', 'text'),
            ('Property', 'property__name', 'text'),
            ('Unit', 'unit__unit_code', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('End Date', 'end_date', 'date'),
            ('Rent', 'rent_amount', 'money'),
            ('Renewal', 'renewal_probability', 'percent'),
        ),
        detail_fields=(
            ('Lease Code', 'lease_code', 'text'),
            ('Tenant', 'tenant__display_name', 'text'),
            ('Property', 'property__name', 'text'),
            ('Unit', 'unit__unit_code', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Start Date', 'start_date', 'date'),
            ('End Date', 'end_date', 'date'),
            ('Days to Expiry', 'days_to_expiry', 'text'),
            ('Rent Amount', 'rent_amount', 'money'),
            ('Deposit Amount', 'deposit_amount', 'money'),
            ('Service Charge', 'service_charge_amount', 'money'),
            ('Billing Cycle', 'get_billing_cycle_display', 'text'),
            ('Escalation Type', 'escalation_type', 'text'),
            ('Escalation Rate', 'escalation_rate', 'percent'),
            ('Renewal Probability', 'renewal_probability', 'percent'),
            ('Notes', 'notes', 'text'),
        ),
        search_fields=('lease_code', 'tenant__display_name', 'property__name', 'unit__unit_code'),
        order_by=('end_date',),
        property_filter='property_id',
    ),
    'billing': ModuleSpec(
        slug='billing',
        title='Billing',
        subtitle='Accounts receivable, rent invoices, service charge, utility, payment matching, and aging.',
        group='Finance',
        code='BL',
        model=Invoice,
        form=InvoiceForm,
        columns=(
            ('Invoice', 'invoice_number', 'text'),
            ('Tenant', 'tenant__display_name', 'text'),
            ('Property', 'property__name', 'text'),
            ('Due Date', 'due_date', 'date'),
            ('Status', 'get_status_display', 'status'),
            ('Total', 'total_amount', 'money'),
            ('Paid', 'paid_amount', 'money'),
            ('Outstanding', 'outstanding_amount', 'money'),
            ('Aging', 'aging_bucket', 'status'),
        ),
        detail_fields=(
            ('Invoice Number', 'invoice_number', 'text'),
            ('Tenant', 'tenant__display_name', 'text'),
            ('Property', 'property__name', 'text'),
            ('Lease', 'lease', 'text'),
            ('Line Type', 'get_line_type_display', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Issue Date', 'issue_date', 'date'),
            ('Due Date', 'due_date', 'date'),
            ('Subtotal', 'subtotal', 'money'),
            ('Tax', 'tax', 'money'),
            ('Discount', 'discount', 'money'),
            ('Total', 'total_amount', 'money'),
            ('Paid', 'paid_amount', 'money'),
            ('Outstanding', 'outstanding_amount', 'money'),
            ('Aging Bucket', 'aging_bucket', 'status'),
            ('Reminder Count', 'reminder_count', 'text'),
            ('Notes', 'notes', 'text'),
        ),
        search_fields=('invoice_number', 'tenant__display_name', 'property__name', 'lease__lease_code'),
        order_by=('-due_date',),
        property_filter='property_id',
    ),
    'vendors': ModuleSpec(
        slug='vendors',
        title='Vendors',
        subtitle='Vendor master, category, SLA, contact, rating, and activation status.',
        group='Execution',
        code='VD',
        model=Vendor,
        form=VendorForm,
        columns=(
            ('Vendor', 'name', 'text'),
            ('Code', 'vendor_code', 'text'),
            ('Category', 'get_category_display', 'text'),
            ('Contact', 'contact_person', 'text'),
            ('SLA', 'sla_hours', 'text'),
            ('Rating', 'rating', 'text'),
            ('Active', 'is_active', 'bool'),
        ),
        detail_fields=(
            ('Vendor Code', 'vendor_code', 'text'),
            ('Name', 'name', 'text'),
            ('Category', 'get_category_display', 'text'),
            ('Contact', 'contact_person', 'text'),
            ('Phone', 'phone', 'text'),
            ('Email', 'email', 'text'),
            ('SLA Hours', 'sla_hours', 'text'),
            ('Rating', 'rating', 'text'),
            ('Active', 'is_active', 'bool'),
        ),
        search_fields=('name', 'vendor_code', 'contact_person', 'email'),
        order_by=('name',),
    ),
    'maintenance': ModuleSpec(
        slug='maintenance',
        title='Maintenance',
        subtitle='Work order queue, vendor assignment, SLA, cost control, owner approval, and evidence rules.',
        group='Execution',
        code='MT',
        model=WorkOrder,
        form=WorkOrderForm,
        columns=(
            ('WO', 'work_order_number', 'text'),
            ('Title', 'title', 'text'),
            ('Property', 'property__name', 'text'),
            ('Priority', 'get_priority_display', 'status'),
            ('Status', 'get_status_display', 'status'),
            ('Due', 'due_at', 'datetime'),
            ('Vendor', 'vendor', 'text'),
            ('Est. Cost', 'estimated_cost', 'money'),
        ),
        detail_fields=(
            ('WO Number', 'work_order_number', 'text'),
            ('Title', 'title', 'text'),
            ('Property', 'property__name', 'text'),
            ('Unit', 'unit', 'text'),
            ('Tenant', 'tenant', 'text'),
            ('Vendor', 'vendor', 'text'),
            ('Priority', 'get_priority_display', 'status'),
            ('Category', 'get_category_display', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Reported At', 'reported_at', 'datetime'),
            ('Due At', 'due_at', 'datetime'),
            ('Requester', 'requester', 'text'),
            ('Estimated Cost', 'estimated_cost', 'money'),
            ('Approved Budget', 'approved_budget', 'money'),
            ('Actual Cost', 'actual_cost', 'money'),
            ('Owner Approval', 'requires_owner_approval', 'bool'),
            ('Before Photo Required', 'before_photo_required', 'bool'),
            ('After Photo Required', 'after_photo_required', 'bool'),
            ('Description', 'description', 'text'),
        ),
        search_fields=('work_order_number', 'title', 'description', 'property__name', 'unit__unit_code', 'requester'),
        order_by=('status', '-reported_at'),
        property_filter='property_id',
    ),
    'inspections': ModuleSpec(
        slug='inspections',
        title='Inspections',
        subtitle='Inspection calendar, compliance scope, score, findings, corrective action, and evidence readiness.',
        group='Execution',
        code='IN',
        model=Inspection,
        form=InspectionForm,
        columns=(
            ('Inspection', 'inspection_number', 'text'),
            ('Scope', 'scope', 'text'),
            ('Property', 'property__name', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Scheduled', 'scheduled_date', 'date'),
            ('Inspector', 'inspector', 'text'),
            ('Score', 'score', 'percent'),
        ),
        detail_fields=(
            ('Inspection Number', 'inspection_number', 'text'),
            ('Scope', 'scope', 'text'),
            ('Property', 'property__name', 'text'),
            ('Unit', 'unit', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Scheduled Date', 'scheduled_date', 'date'),
            ('Completed Date', 'completed_date', 'date'),
            ('Inspector', 'inspector', 'text'),
            ('Score', 'score', 'percent'),
            ('Notes', 'notes', 'text'),
        ),
        search_fields=('inspection_number', 'scope', 'property__name', 'inspector'),
        order_by=('scheduled_date',),
        property_filter='property_id',
    ),
    'documents': ModuleSpec(
        slug='documents',
        title='Documents',
        subtitle='Lease documents, KYC, handover, insurance, tax, expiry monitoring, and document owner.',
        group='Execution',
        code='DC',
        model=Document,
        form=DocumentForm,
        columns=(
            ('Document', 'document_number', 'text'),
            ('Title', 'title', 'text'),
            ('Type', 'get_document_type_display', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Owner', 'owner', 'text'),
            ('Expiry', 'expiry_date', 'date'),
            ('Property', 'property', 'text'),
        ),
        detail_fields=(
            ('Document Number', 'document_number', 'text'),
            ('Title', 'title', 'text'),
            ('Type', 'get_document_type_display', 'text'),
            ('Status', 'get_status_display', 'status'),
            ('Property', 'property', 'text'),
            ('Tenant', 'tenant', 'text'),
            ('Lease', 'lease', 'text'),
            ('Owner', 'owner', 'text'),
            ('Expiry Date', 'expiry_date', 'date'),
            ('Storage URL', 'storage_url', 'text'),
            ('Notes', 'notes', 'text'),
        ),
        search_fields=('document_number', 'title', 'owner', 'property__name', 'tenant__display_name'),
        order_by=('expiry_date', 'title'),
        property_filter='property_id',
    ),
    'approvals': ModuleSpec(
        slug='approvals',
        title='Approvals',
        subtitle='Approval queue for capex, discounts, write-offs, lease exceptions, and owner-sensitive actions.',
        group='Control',
        code='AP',
        model=ApprovalRequest,
        form=ApprovalRequestForm,
        columns=(
            ('Request', 'request_number', 'text'),
            ('Title', 'title', 'text'),
            ('Property', 'property__name', 'text'),
            ('Object', 'object_reference', 'text'),
            ('Amount', 'amount', 'money'),
            ('Approver', 'approver_name', 'text'),
            ('Due', 'due_date', 'date'),
            ('Status', 'get_status_display', 'status'),
        ),
        detail_fields=(
            ('Request Number', 'request_number', 'text'),
            ('Title', 'title', 'text'),
            ('Property', 'property__name', 'text'),
            ('Object Type', 'object_type', 'text'),
            ('Object Reference', 'object_reference', 'text'),
            ('Requested By', 'requested_by', 'text'),
            ('Approver', 'approver_name', 'text'),
            ('Amount', 'amount', 'money'),
            ('Status', 'get_status_display', 'status'),
            ('Due Date', 'due_date', 'date'),
            ('Decision Note', 'decision_note', 'text'),
        ),
        search_fields=('request_number', 'title', 'object_reference', 'requested_by', 'approver_name'),
        order_by=('status', 'due_date'),
        property_filter='property_id',
    ),
}


NAV_GROUPS = [
    {'title': title, 'items': [spec for spec in MODULES.values() if spec.group == title]}
    for title in ['Operations', 'Finance', 'Execution', 'Control']
]


class PmsContextMixin:
    active_module = 'dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_groups'] = NAV_GROUPS
        context['active_module'] = self.active_module
        context['properties'] = Property.objects.all()
        return context


class DashboardView(LoginRequiredMixin, PmsContextMixin, TemplateView):
    template_name = 'pms/dashboard.html'
    active_module = 'dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_id = self.request.GET.get('property') or 'all'
        selected_property = None
        property_qs = Property.objects.prefetch_related('units', 'leases')
        if property_id != 'all':
            selected_property = get_object_or_404(Property, pk=property_id)
            property_qs = property_qs.filter(pk=selected_property.pk)

        invoice_qs = Invoice.objects.select_related('tenant', 'property')
        work_qs = WorkOrder.objects.select_related('property', 'unit', 'vendor')
        lease_qs = Lease.objects.select_related('tenant', 'property', 'unit')
        if selected_property:
            invoice_qs = invoice_qs.filter(property=selected_property)
            work_qs = work_qs.filter(property=selected_property)
            lease_qs = lease_qs.filter(property=selected_property)

        total_units = sum(prop.total_units for prop in property_qs)
        occupied_units = sum(prop.occupied_units for prop in property_qs)
        occupancy_rate = round((occupied_units / total_units) * 100) if total_units else 0
        rent_roll = sum((prop.active_rent_roll for prop in property_qs), Decimal('0'))
        outstanding = sum((invoice.outstanding_amount for invoice in invoice_qs), Decimal('0'))
        deposits = sum((lease.deposit_amount for lease in lease_qs.filter(status__in=[Lease.Status.ACTIVE, Lease.Status.RENEWAL])), Decimal('0'))
        active_work = work_qs.exclude(status__in=[WorkOrder.Status.CLOSED, WorkOrder.Status.CANCELLED])

        aging_buckets = []
        for bucket in ['Current', '1-30', '31-60', '61-90', '90+']:
            bucket_invoices = [invoice for invoice in invoice_qs if invoice.aging_bucket == bucket]
            bucket_amount = sum((invoice.outstanding_amount for invoice in bucket_invoices), Decimal('0'))
            aging_buckets.append(
                {
                    'label': bucket,
                    'count': len(bucket_invoices),
                    'amount': money(bucket_amount),
                    'width': min(100, int((bucket_amount / outstanding) * 100)) if outstanding else 0,
                }
            )

        lease_lanes = []
        for status in [Lease.Status.ACTIVE, Lease.Status.RENEWAL, Lease.Status.NOTICE, Lease.Status.COLLECTION]:
            lane_items = lease_qs.filter(status=status).order_by('end_date')[:6]
            lease_lanes.append({'label': Lease.Status(status).label, 'items': lane_items})

        context.update(
            {
                'selected_property_id': property_id,
                'selected_property': selected_property,
                'metric_cards': [
                    {'label': 'Monthly Rent Roll', 'value': money(rent_roll), 'detail': f'{occupied_units} occupied dari {total_units} unit', 'tone': 'success'},
                    {'label': 'Occupancy', 'value': f'{occupancy_rate}%', 'detail': 'Dihitung dari active unit status', 'tone': 'success'},
                    {'label': 'Outstanding AR', 'value': money(outstanding), 'detail': f'{invoice_qs.exclude(status=Invoice.Status.PAID).count()} invoice belum clear', 'tone': 'warning'},
                    {'label': 'Open Work Orders', 'value': str(active_work.count()), 'detail': f'{active_work.filter(priority=WorkOrder.Priority.EMERGENCY).count()} emergency ticket', 'tone': 'danger'},
                    {'label': 'Deposit Held', 'value': money(deposits), 'detail': 'Deposit aktif dan renewal', 'tone': 'neutral'},
                    {'label': 'Approvals', 'value': str(ApprovalRequest.objects.filter(status=ApprovalRequest.Status.PENDING).count()), 'detail': 'Menunggu keputusan owner/manager', 'tone': 'warning'},
                ],
                'portfolio_rows': property_qs,
                'aging_buckets': aging_buckets,
                'work_orders': active_work[:8],
                'lease_lanes': lease_lanes,
                'activity_events': ActivityEvent.objects.select_related('property')[:8],
                'documents_due': Document.objects.exclude(status=Document.Status.COMPLETE).order_by('expiry_date')[:6],
                'approvals': ApprovalRequest.objects.select_related('property').filter(status=ApprovalRequest.Status.PENDING)[:6],
            }
        )
        return context


class ModuleMixin(LoginRequiredMixin, PmsContextMixin):
    spec: ModuleSpec

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        module = kwargs.get('module')
        try:
            self.spec = MODULES[module]
        except KeyError as exc:
            raise Http404('Module tidak ditemukan') from exc
        self.active_module = self.spec.slug
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spec'] = self.spec
        return context


class ModuleListView(ModuleMixin, ListView):
    template_name = 'pms/list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = self.spec.model.objects.all().order_by(*self.spec.order_by)
        property_id = self.request.GET.get('property')
        if property_id and property_id != 'all' and self.spec.property_filter:
            queryset = queryset.filter(**{self.spec.property_filter: property_id})
        query = self.request.GET.get('q', '').strip()
        if query:
            q_object = Q()
            for field in self.spec.search_fields:
                q_object |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(q_object)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_property_id'] = self.request.GET.get('property', 'all')
        context['columns'] = self.spec.columns
        context['rows'] = [
            {
                'object': obj,
                'cells': [
                    {
                        'label': label,
                        'value': display_value(obj, path, kind),
                        'kind': kind,
                        'tone': status_tone(display_value(obj, path, kind)) if kind == 'status' else '',
                    }
                    for label, path, kind in self.spec.columns
                ],
            }
            for obj in context['object_list']
        ]
        return context


class ModuleDetailView(ModuleMixin, DetailView):
    template_name = 'pms/detail.html'

    def get_queryset(self):
        return self.spec.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context['object']
        context['facts'] = [
            {
                'label': label,
                'value': display_value(obj, path, kind),
                'kind': kind,
                'tone': status_tone(display_value(obj, path, kind)) if kind == 'status' else '',
            }
            for label, path, kind in self.spec.detail_fields
        ]
        if isinstance(obj, Property):
            context['related_cards'] = [
                {'label': 'Units', 'value': obj.total_units, 'detail': f'{obj.occupied_units} occupied'},
                {'label': 'Rent Roll', 'value': money(obj.active_rent_roll), 'detail': 'Active leases'},
                {'label': 'Open WO', 'value': obj.work_orders.exclude(status=WorkOrder.Status.CLOSED).count(), 'detail': 'Maintenance queue'},
                {'label': 'Documents', 'value': obj.documents.count(), 'detail': 'Vault records'},
            ]
        elif isinstance(obj, Tenant):
            context['related_cards'] = [
                {'label': 'Outstanding', 'value': money(obj.outstanding_balance), 'detail': 'Open invoices'},
                {'label': 'Leases', 'value': obj.leases.count(), 'detail': 'Lease history'},
                {'label': 'Documents', 'value': obj.documents.count(), 'detail': 'KYC and legal docs'},
            ]
        else:
            context['related_cards'] = []
        return context


class ModuleCreateView(ModuleMixin, CreateView):
    template_name = 'pms/form.html'

    def get_form_class(self):
        return self.spec.form

    def get_success_url(self):
        return reverse('pms:module_list', kwargs={'module': self.spec.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{self.spec.title} berhasil dibuat.')
        return response


class ModuleUpdateView(ModuleMixin, UpdateView):
    template_name = 'pms/form.html'

    def get_queryset(self):
        return self.spec.model.objects.all()

    def get_form_class(self):
        return self.spec.form

    def get_success_url(self):
        return reverse('pms:module_detail', kwargs={'module': self.spec.slug, 'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{self.spec.title} berhasil diperbarui.')
        return response


class WorkOrderTransitionView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int, status: str) -> HttpResponseRedirect:
        work_order = get_object_or_404(WorkOrder, pk=pk)
        valid_statuses = {choice.value for choice in WorkOrder.Status}
        if status not in valid_statuses:
            raise Http404('Status work order tidak valid')
        previous = work_order.get_status_display()
        work_order.status = status
        work_order.save(update_fields=['status', 'updated_at'])
        ActivityEvent.objects.create(
            property=work_order.property,
            event_type=ActivityEvent.Type.WORK_ORDER,
            title=f'{work_order.work_order_number} moved to {work_order.get_status_display()}',
            description=f'Status berubah dari {previous} ke {work_order.get_status_display()}.',
            actor=request.user.get_full_name() or request.user.username,
        )
        messages.success(request, f'{work_order.work_order_number} dipindahkan ke {work_order.get_status_display()}.')
        return redirect(work_order.get_absolute_url())


class ReportsView(LoginRequiredMixin, PmsContextMixin, TemplateView):
    template_name = 'pms/reports.html'
    active_module = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packs'] = [
            {
                'title': 'Owner Statement',
                'description': 'NOI, rent roll, escrow, reserve, payout owner, dan capex reserve.',
                'metrics': ['Rent roll', 'NOI', 'Deposit held', 'Owner payout'],
            },
            {
                'title': 'Delinquency Pack',
                'description': 'Aging AR, reminder history, promise-to-pay, dan legal escalation.',
                'metrics': ['Outstanding', 'Aging bucket', 'Reminder', 'Commitment'],
            },
            {
                'title': 'Asset Health',
                'description': 'SLA maintenance, recurring fault, inspection finding, dan forecast capex.',
                'metrics': ['Open WO', 'SLA breach', 'Inspection score', 'Vendor rating'],
            },
            {
                'title': 'Lease Expiry Book',
                'description': 'Rolling 30/60/90 hari untuk renewal, notice, vacancy risk, dan projected rent.',
                'metrics': ['Expiry', 'Renewal probability', 'Market rent gap', 'Make-ready date'],
            },
        ]
        return context


def redirect_dashboard(request: HttpRequest) -> HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect('pms:dashboard')
    return redirect(reverse_lazy('login'))
