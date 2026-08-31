from django import forms

from .models import (
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


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class StyledModelForm(forms.ModelForm):
    date_fields: tuple[str, ...] = ()
    datetime_fields: tuple[str, ...] = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('placeholder', field.label)
            if name in self.date_fields:
                field.widget = DateInput(attrs=field.widget.attrs)
            if name in self.datetime_fields:
                field.widget = DateTimeInput(attrs=field.widget.attrs)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'checkbox-control'


class OrganizationForm(StyledModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'legal_name', 'tax_id', 'default_currency', 'email', 'phone', 'address']


class PropertyForm(StyledModelForm):
    class Meta:
        model = Property
        fields = [
            'organization',
            'property_code',
            'name',
            'property_type',
            'status',
            'address',
            'city',
            'province',
            'postal_code',
            'manager_name',
            'manager_email',
            'gross_area_sqm',
            'net_leasable_area_sqm',
            'service_charge_rate',
            'sinking_fund_rate',
            'owner_statement_day',
        ]


class UnitForm(StyledModelForm):
    class Meta:
        model = Unit
        fields = [
            'property',
            'unit_code',
            'floor',
            'unit_type',
            'area_sqm',
            'bedrooms',
            'bathrooms',
            'status',
            'market_rent',
            'current_rent',
            'handover_state',
            'meter_electric',
            'meter_water',
            'next_action',
        ]


class TenantForm(StyledModelForm):
    date_fields = ('last_contact_date',)

    class Meta:
        model = Tenant
        fields = [
            'organization',
            'tenant_code',
            'tenant_type',
            'display_name',
            'legal_name',
            'tax_id',
            'email',
            'phone',
            'billing_address',
            'risk_level',
            'kyc_status',
            'tenant_health_score',
            'last_contact_date',
            'notes',
        ]


class LeaseForm(StyledModelForm):
    date_fields = ('start_date', 'end_date')

    class Meta:
        model = Lease
        fields = [
            'property',
            'unit',
            'tenant',
            'lease_code',
            'status',
            'start_date',
            'end_date',
            'rent_amount',
            'deposit_amount',
            'service_charge_amount',
            'billing_cycle',
            'escalation_type',
            'escalation_rate',
            'renewal_probability',
            'signed_document',
            'notes',
        ]

    def clean(self):
        cleaned = super().clean()
        property_obj = cleaned.get('property')
        unit = cleaned.get('unit')
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')
        if property_obj and unit and unit.property_id != property_obj.id:
            self.add_error('unit', 'Unit harus berada di properti yang sama dengan lease.')
        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', 'Tanggal selesai harus setelah tanggal mulai.')
        return cleaned


class InvoiceForm(StyledModelForm):
    date_fields = ('issue_date', 'due_date')

    class Meta:
        model = Invoice
        fields = [
            'property',
            'tenant',
            'lease',
            'invoice_number',
            'line_type',
            'status',
            'issue_date',
            'due_date',
            'subtotal',
            'tax',
            'discount',
            'paid_amount',
            'reminder_count',
            'notes',
        ]


class VendorForm(StyledModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'category', 'contact_person', 'phone', 'email', 'sla_hours', 'rating', 'is_active']


class WorkOrderForm(StyledModelForm):
    datetime_fields = ('reported_at', 'due_at')

    class Meta:
        model = WorkOrder
        fields = [
            'property',
            'unit',
            'tenant',
            'vendor',
            'work_order_number',
            'title',
            'description',
            'priority',
            'category',
            'status',
            'reported_at',
            'due_at',
            'requester',
            'estimated_cost',
            'approved_budget',
            'actual_cost',
            'requires_owner_approval',
            'before_photo_required',
            'after_photo_required',
        ]


class InspectionForm(StyledModelForm):
    date_fields = ('scheduled_date', 'completed_date')

    class Meta:
        model = Inspection
        fields = ['property', 'unit', 'inspection_number', 'scope', 'status', 'scheduled_date', 'completed_date', 'inspector', 'score', 'notes']


class DocumentForm(StyledModelForm):
    date_fields = ('expiry_date',)

    class Meta:
        model = Document
        fields = ['property', 'tenant', 'lease', 'document_number', 'title', 'document_type', 'status', 'owner', 'expiry_date', 'storage_url', 'notes']


class ApprovalRequestForm(StyledModelForm):
    date_fields = ('due_date',)

    class Meta:
        model = ApprovalRequest
        fields = [
            'request_number',
            'property',
            'object_type',
            'object_reference',
            'title',
            'requested_by',
            'approver_name',
            'amount',
            'status',
            'due_date',
            'decision_note',
        ]
