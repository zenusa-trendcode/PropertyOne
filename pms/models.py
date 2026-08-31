from builtins import property as builtin_property
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    name = models.CharField(max_length=160)
    legal_name = models.CharField(max_length=220, blank=True)
    tax_id = models.CharField(max_length=80, blank=True)
    default_currency = models.CharField(max_length=3, default='IDR')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Property(TimeStampedModel):
    class Type(models.TextChoices):
        APARTMENT = 'APARTMENT', 'Apartemen'
        OFFICE = 'OFFICE', 'Komersial'
        TOWNHOUSE = 'TOWNHOUSE', 'Townhouse'
        VILLA = 'VILLA', 'Serviced Villa'
        MIXED = 'MIXED', 'Mixed Use'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        STABILIZED = 'STABILIZED', 'Stabilized'
        LEASE_UP = 'LEASE_UP', 'Lease Up'
        WATCHLIST = 'WATCHLIST', 'Watchlist'
        INACTIVE = 'INACTIVE', 'Inactive'

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='properties')
    property_code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=180)
    property_type = models.CharField(max_length=24, choices=Type.choices)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.ACTIVE)
    address = models.TextField()
    city = models.CharField(max_length=80)
    province = models.CharField(max_length=80, blank=True)
    postal_code = models.CharField(max_length=16, blank=True)
    manager_name = models.CharField(max_length=120)
    manager_email = models.EmailField(blank=True)
    gross_area_sqm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_leasable_area_sqm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    service_charge_rate = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    sinking_fund_rate = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    owner_statement_day = models.PositiveSmallIntegerField(default=7)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'properties'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'properties', 'pk': self.pk})

    @builtin_property
    def total_units(self) -> int:
        return self.units.count()

    @builtin_property
    def occupied_units(self) -> int:
        return self.units.filter(status__in=[Unit.Status.OCCUPIED, Unit.Status.NOTICE]).count()

    @builtin_property
    def occupancy_rate(self) -> int:
        if not self.total_units:
            return 0
        return round((self.occupied_units / self.total_units) * 100)

    @builtin_property
    def active_rent_roll(self) -> Decimal:
        return sum((lease.rent_amount for lease in self.leases.active()), Decimal('0'))


class Unit(TimeStampedModel):
    class Type(models.TextChoices):
        STUDIO = 'STUDIO', 'Studio'
        ONE_BR = 'ONE_BR', '1BR'
        TWO_BR = 'TWO_BR', '2BR'
        THREE_BR = 'THREE_BR', '3BR'
        RETAIL = 'RETAIL', 'Retail'
        OFFICE = 'OFFICE', 'Office'
        STORAGE = 'STORAGE', 'Storage'
        VILLA = 'VILLA', 'Villa'

    class Status(models.TextChoices):
        VACANT = 'VACANT', 'Vacant'
        MAKE_READY = 'MAKE_READY', 'Make Ready'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        NOTICE = 'NOTICE', 'Notice'
        DELINQUENT = 'DELINQUENT', 'Delinquent'
        OFFLINE = 'OFFLINE', 'Offline'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_code = models.CharField(max_length=40)
    floor = models.CharField(max_length=24, blank=True)
    unit_type = models.CharField(max_length=24, choices=Type.choices)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.VACANT)
    market_rent = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    current_rent = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    handover_state = models.CharField(max_length=120, blank=True)
    meter_electric = models.CharField(max_length=80, blank=True)
    meter_water = models.CharField(max_length=80, blank=True)
    next_action = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ['property__name', 'unit_code']
        constraints = [
            models.UniqueConstraint(fields=['property', 'unit_code'], name='unique_unit_per_property'),
        ]

    def __str__(self) -> str:
        return f'{self.property.property_code}-{self.unit_code}'

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'units', 'pk': self.pk})


class Tenant(TimeStampedModel):
    class Type(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        COMPANY = 'COMPANY', 'Company'

    class Risk(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Excellent'
        MONITOR = 'MONITOR', 'Monitor'
        AT_RISK = 'AT_RISK', 'At Risk'

    class KycStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PARTIAL = 'PARTIAL', 'Partial'
        COMPLETE = 'COMPLETE', 'Complete'
        EXPIRED = 'EXPIRED', 'Expired'

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='tenants')
    tenant_code = models.CharField(max_length=32, unique=True)
    tenant_type = models.CharField(max_length=24, choices=Type.choices)
    display_name = models.CharField(max_length=180)
    legal_name = models.CharField(max_length=220, blank=True)
    tax_id = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    billing_address = models.TextField(blank=True)
    risk_level = models.CharField(max_length=24, choices=Risk.choices, default=Risk.EXCELLENT)
    kyc_status = models.CharField(max_length=24, choices=KycStatus.choices, default=KycStatus.PENDING)
    tenant_health_score = models.PositiveSmallIntegerField(default=80)
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['display_name']

    def __str__(self) -> str:
        return self.display_name

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'tenants', 'pk': self.pk})

    @builtin_property
    def outstanding_balance(self) -> Decimal:
        return sum((invoice.outstanding_amount for invoice in self.invoices.all()), Decimal('0'))


class ActiveLeaseQuerySet(models.QuerySet):
    def active(self):
        today = timezone.localdate()
        return self.filter(status__in=[Lease.Status.ACTIVE, Lease.Status.RENEWAL], start_date__lte=today, end_date__gte=today)


class Lease(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        RENEWAL = 'RENEWAL', 'Renewal Offered'
        NOTICE = 'NOTICE', 'Move Out Notice'
        COLLECTION = 'COLLECTION', 'Collection Hold'
        EXPIRED = 'EXPIRED', 'Expired'
        TERMINATED = 'TERMINATED', 'Terminated'

    class BillingCycle(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Monthly'
        QUARTERLY = 'QUARTERLY', 'Quarterly'
        ANNUAL = 'ANNUAL', 'Annual'

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='leases')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='leases')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='leases')
    lease_code = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=16, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    service_charge_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    escalation_type = models.CharField(max_length=80, blank=True)
    escalation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    renewal_probability = models.PositiveSmallIntegerField(default=50)
    signed_document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='signed_leases')
    notes = models.TextField(blank=True)

    objects = ActiveLeaseQuerySet.as_manager()

    class Meta:
        ordering = ['end_date', 'lease_code']

    def __str__(self) -> str:
        return self.lease_code

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'leases', 'pk': self.pk})

    @builtin_property
    def days_to_expiry(self) -> int:
        return (self.end_date - timezone.localdate()).days


class Invoice(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ISSUED = 'ISSUED', 'Issued'
        PARTIAL = 'PARTIAL', 'Partially Paid'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'
        ESCALATED = 'ESCALATED', 'Escalated'
        VOID = 'VOID', 'Void'

    class LineType(models.TextChoices):
        RENT = 'RENT', 'Rent'
        SERVICE = 'SERVICE', 'Service Charge'
        DEPOSIT = 'DEPOSIT', 'Deposit'
        UTILITY = 'UTILITY', 'Utility'
        PENALTY = 'PENALTY', 'Penalty'
        OTHER = 'OTHER', 'Other'

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='invoices')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='invoices')
    lease = models.ForeignKey(Lease, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    invoice_number = models.CharField(max_length=40, unique=True)
    line_type = models.CharField(max_length=24, choices=LineType.choices, default=LineType.RENT)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    issue_date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    tax = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    reminder_count = models.PositiveSmallIntegerField(default=0)
    last_reminder_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-due_date', 'invoice_number']

    def __str__(self) -> str:
        return self.invoice_number

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'billing', 'pk': self.pk})

    @builtin_property
    def total_amount(self) -> Decimal:
        return self.subtotal + self.tax - self.discount

    @builtin_property
    def outstanding_amount(self) -> Decimal:
        amount = self.total_amount - self.paid_amount
        return amount if amount > 0 else Decimal('0')

    @builtin_property
    def aging_bucket(self) -> str:
        if self.outstanding_amount == 0:
            return 'Current'
        days = (timezone.localdate() - self.due_date).days
        if days <= 0:
            return 'Current'
        if days <= 30:
            return '1-30'
        if days <= 60:
            return '31-60'
        if days <= 90:
            return '61-90'
        return '90+'


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        VIRTUAL_ACCOUNT = 'VIRTUAL_ACCOUNT', 'Virtual Account'
        CARD = 'CARD', 'Card'
        CASH = 'CASH', 'Cash'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    method = models.CharField(max_length=24, choices=Method.choices)
    reference = models.CharField(max_length=120)
    matched_by = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self) -> str:
        return f'{self.reference} - {self.amount}'


class Vendor(TimeStampedModel):
    class Category(models.TextChoices):
        HVAC = 'HVAC', 'HVAC'
        ELECTRICAL = 'ELECTRICAL', 'Electrical'
        PLUMBING = 'PLUMBING', 'Plumbing'
        SECURITY = 'SECURITY', 'Security'
        CLEANING = 'CLEANING', 'Cleaning'
        GENERAL = 'GENERAL', 'General Contractor'

    vendor_code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=180)
    category = models.CharField(max_length=24, choices=Category.choices)
    contact_person = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    sla_hours = models.PositiveSmallIntegerField(default=24)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('4.00'))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class WorkOrder(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        EMERGENCY = 'EMERGENCY', 'Emergency'
        PREVENTIVE = 'PREVENTIVE', 'Preventive'

    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        TRIAGED = 'TRIAGED', 'Triaged'
        APPROVAL = 'APPROVAL', 'Waiting Approval'
        ASSIGNED = 'ASSIGNED', 'Vendor Assigned'
        PARTS = 'PARTS', 'Waiting Parts'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        QA = 'QA', 'QA Review'
        CLOSED = 'CLOSED', 'Closed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class Category(models.TextChoices):
        HVAC = 'HVAC', 'HVAC'
        ELECTRICAL = 'ELECTRICAL', 'Electrical'
        PLUMBING = 'PLUMBING', 'Plumbing'
        STRUCTURAL = 'STRUCTURAL', 'Structural'
        CLEANING = 'CLEANING', 'Cleaning'
        SECURITY = 'SECURITY', 'Security'
        OTHER = 'OTHER', 'Other'

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='work_orders')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    work_order_number = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=180)
    description = models.TextField()
    priority = models.CharField(max_length=24, choices=Priority.choices, default=Priority.MEDIUM)
    category = models.CharField(max_length=24, choices=Category.choices, default=Category.OTHER)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.NEW)
    reported_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    requester = models.CharField(max_length=120, blank=True)
    estimated_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    approved_budget = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    requires_owner_approval = models.BooleanField(default=False)
    before_photo_required = models.BooleanField(default=True)
    after_photo_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['status', '-reported_at']

    def __str__(self) -> str:
        return self.work_order_number

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'maintenance', 'pk': self.pk})

    @builtin_property
    def is_overdue(self) -> bool:
        return bool(self.due_at and self.status not in [self.Status.CLOSED, self.Status.CANCELLED] and self.due_at < timezone.now())


class Inspection(TimeStampedModel):
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        NEEDS_ACTION = 'NEEDS_ACTION', 'Needs Action'
        CRITICAL = 'CRITICAL', 'Critical'
        COMPLETE = 'COMPLETE', 'Complete'

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='inspections')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections')
    inspection_number = models.CharField(max_length=40, unique=True)
    scope = models.CharField(max_length=180)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.SCHEDULED)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    inspector = models.CharField(max_length=120)
    score = models.PositiveSmallIntegerField(default=100)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['scheduled_date']

    def __str__(self) -> str:
        return self.inspection_number

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'inspections', 'pk': self.pk})


class InspectionFinding(TimeStampedModel):
    class Severity(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        RESOLVED = 'RESOLVED', 'Resolved'
        WAIVED = 'WAIVED', 'Waived'

    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='findings')
    severity = models.CharField(max_length=24, choices=Severity.choices)
    title = models.CharField(max_length=180)
    corrective_action = models.TextField(blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.OPEN)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['status', '-severity']

    def __str__(self) -> str:
        return self.title


class Document(TimeStampedModel):
    class Type(models.TextChoices):
        LEASE = 'LEASE', 'Lease'
        KYC = 'KYC', 'Tenant KYC'
        HANDOVER = 'HANDOVER', 'Handover'
        ASSET = 'ASSET', 'Asset'
        INSURANCE = 'INSURANCE', 'Insurance'
        TAX = 'TAX', 'Tax'
        VENDOR = 'VENDOR', 'Vendor'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending'
        REVIEW = 'REVIEW', 'Review'
        COMPLETE = 'COMPLETE', 'Complete'
        EXPIRED = 'EXPIRED', 'Expired'

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    lease = models.ForeignKey(Lease, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    document_number = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=180)
    document_type = models.CharField(max_length=24, choices=Type.choices)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    owner = models.CharField(max_length=120, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    storage_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['expiry_date', 'title']

    def __str__(self) -> str:
        return self.document_number

    def get_absolute_url(self) -> str:
        return reverse('pms:module_detail', kwargs={'module': 'documents', 'pk': self.pk})


class ApprovalRequest(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    request_number = models.CharField(max_length=40, unique=True)
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='approvals')
    object_type = models.CharField(max_length=80)
    object_reference = models.CharField(max_length=80)
    title = models.CharField(max_length=180)
    requested_by = models.CharField(max_length=120)
    approver_name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField(null=True, blank=True)
    decision_note = models.TextField(blank=True)

    class Meta:
        ordering = ['status', 'due_date']

    def __str__(self) -> str:
        return self.request_number


class ActivityEvent(TimeStampedModel):
    class Type(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        WORK_ORDER = 'WORK_ORDER', 'Work Order'
        LEASE = 'LEASE', 'Lease'
        INSPECTION = 'INSPECTION', 'Inspection'
        DOCUMENT = 'DOCUMENT', 'Document'
        SYSTEM = 'SYSTEM', 'System'

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_events')
    event_type = models.CharField(max_length=24, choices=Type.choices)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    actor = models.CharField(max_length=120, blank=True)
    event_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-event_time']

    def __str__(self) -> str:
        return self.title
