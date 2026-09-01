from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ActivityEvent, Invoice, Unit, WorkOrder


class PmsSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', stdout=StringIO())

    def setUp(self):
        self.client.login(username='admin', password='Admin12345!')

    def test_seed_creates_demo_admin(self):
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='admin', is_superuser=True).exists())

    def test_dashboard_renders_operational_metrics(self):
        response = self.client.get(reverse('pms:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monthly Rent Roll')
        self.assertContains(response, 'Portfolio Performance')
        self.assertContains(response, 'Lease Pipeline')

    def test_module_search_filters_units(self):
        response = self.client.get(reverse('pms:module_list', kwargs={'module': 'units'}), {'q': 'A-1207'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A-1207')
        self.assertNotContains(response, 'O-1702')

    def test_invoice_aging_bucket_is_business_aware(self):
        invoice = Invoice.objects.get(invoice_number='INV-0726-044')
        invoice.due_date = timezone.localdate() - timedelta(days=45)
        self.assertEqual(invoice.aging_bucket, '31-60')
        self.assertGreater(invoice.outstanding_amount, 0)

    def test_work_order_transition_creates_activity_event(self):
        work_order = WorkOrder.objects.get(work_order_number='WO-1039')
        response = self.client.post(
            reverse('pms:work_order_transition', kwargs={'pk': work_order.pk, 'status': WorkOrder.Status.IN_PROGRESS})
        )
        self.assertRedirects(response, work_order.get_absolute_url())
        work_order.refresh_from_db()
        self.assertEqual(work_order.status, WorkOrder.Status.IN_PROGRESS)
        self.assertTrue(ActivityEvent.objects.filter(title__contains='WO-1039').exists())

    def test_property_filter_scopes_unit_list(self):
        unit = Unit.objects.get(unit_code='V-09')
        response = self.client.get(reverse('pms:module_list', kwargs={'module': 'units'}), {'property': unit.property_id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'V-09')
        self.assertNotContains(response, 'A-1207')
