from django.contrib import admin

from .models import (
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


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_name', 'default_currency', 'email']
    search_fields = ['name', 'legal_name', 'tax_id']


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    fields = ['unit_code', 'unit_type', 'area_sqm', 'status', 'market_rent', 'current_rent']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_code', 'name', 'property_type', 'city', 'status', 'manager_name']
    list_filter = ['property_type', 'status', 'city']
    search_fields = ['property_code', 'name', 'city', 'manager_name']
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit_code', 'property', 'unit_type', 'area_sqm', 'status', 'market_rent', 'current_rent']
    list_filter = ['property', 'unit_type', 'status']
    search_fields = ['unit_code', 'property__name']


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['tenant_code', 'display_name', 'tenant_type', 'risk_level', 'kyc_status', 'tenant_health_score']
    list_filter = ['tenant_type', 'risk_level', 'kyc_status']
    search_fields = ['tenant_code', 'display_name', 'legal_name', 'tax_id', 'email']


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['lease_code', 'tenant', 'property', 'unit', 'status', 'start_date', 'end_date', 'rent_amount']
    list_filter = ['status', 'property', 'billing_cycle']
    search_fields = ['lease_code', 'tenant__display_name', 'unit__unit_code']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'tenant', 'property', 'status', 'due_date', 'total_amount', 'paid_amount', 'outstanding_amount']
    list_filter = ['status', 'line_type', 'property']
    search_fields = ['invoice_number', 'tenant__display_name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'invoice', 'payment_date', 'amount', 'method', 'matched_by']
    list_filter = ['method', 'payment_date']
    search_fields = ['reference', 'invoice__invoice_number']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_code', 'name', 'category', 'sla_hours', 'rating', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['vendor_code', 'name', 'contact_person']


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['work_order_number', 'title', 'property', 'unit', 'priority', 'status', 'due_at', 'estimated_cost']
    list_filter = ['priority', 'status', 'category', 'property']
    search_fields = ['work_order_number', 'title', 'description', 'requester']


class InspectionFindingInline(admin.TabularInline):
    model = InspectionFinding
    extra = 0
    fields = ['severity', 'title', 'corrective_action', 'status', 'due_date']


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['inspection_number', 'property', 'scope', 'status', 'scheduled_date', 'score', 'inspector']
    list_filter = ['status', 'property', 'scheduled_date']
    search_fields = ['inspection_number', 'scope', 'inspector']
    inlines = [InspectionFindingInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'title', 'document_type', 'status', 'owner', 'expiry_date']
    list_filter = ['document_type', 'status']
    search_fields = ['document_number', 'title', 'owner']


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'title', 'property', 'amount', 'status', 'approver_name', 'due_date']
    list_filter = ['status', 'property', 'object_type']
    search_fields = ['request_number', 'title', 'object_reference', 'requested_by', 'approver_name']


@admin.register(ActivityEvent)
class ActivityEventAdmin(admin.ModelAdmin):
    list_display = ['event_time', 'event_type', 'title', 'property', 'actor']
    list_filter = ['event_type', 'property']
    search_fields = ['title', 'description', 'actor']
