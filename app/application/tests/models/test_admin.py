from django.contrib.admin.sites import AdminSite
from application.tests.common import ApplicationBaseTestCase
from application.models import CallToAction
from application.admin import CallToActionAdmin
from application.forms import CallToActionAdminForm


class CallToActionAdminTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(CallToActionAdminTestCase, self).setUp()
        self.model_admin = CallToActionAdmin(
            model=CallToAction,
            admin_site=AdminSite()
        )

    def test_properties(self):
        self.assertEqual(self.model_admin.form, CallToActionAdminForm)
        list_display = ['tagline', 'deadline', 'available_for_applications']
        self.assertEqual(self.model_admin.list_display, list_display)
        prepopulated_fields = {'slug': ('tagline',)}
        self.assertEqual(
            self.model_admin.prepopulated_fields,
            prepopulated_fields)
