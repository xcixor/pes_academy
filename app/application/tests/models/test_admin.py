from django.contrib.admin.sites import AdminSite
from application.tests.common import ApplicationBaseTestCase
from application.models import Application
from application.admin import ApplicationAdmin
from application.forms import ApplicationAdminForm


class ApplicationAdminTestCase(ApplicationBaseTestCase):

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
