from django.contrib.admin.sites import AdminSite
from sme.tests.common import SMETestCase
from sme.models import Application
from sme.admin import ApplicationAdmin
from sme.forms import ApplicationAdminForm


class ApplicationAdminTestCase(SMETestCase):

    def setUp(self):
        super(ApplicationAdminTestCase, self).setUp()
        self.model_admin = ApplicationAdmin(
            model=Application,
            admin_site=AdminSite()
        )

    def test_properties(self):
        self.assertEqual(self.model_admin.form, ApplicationAdminForm)
        list_display = ['tagline', 'deadline', 'available_for_applications']
        self.assertEqual(self.model_admin.list_display, list_display)
        prepopulated_fields = {'slug': ('tagline',)}
        self.assertEqual(
            self.model_admin.prepopulated_fields,
            prepopulated_fields)
