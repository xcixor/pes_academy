from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from eligibility.presentation.views import EligibilityView
from eligibility.tests.common import StaffBaseTestCase


class EligibilityViewTestCase(StaffBaseTestCase):

    def setUp(self):
        super(EligibilityViewTestCase, self).setUp()
        self.application = self.create_application_instance()

    def test_view_properties(self):
        self.assertEqual(EligibilityView.template_name,
                         'eligibility/eligibility.html')
        self.assertTrue(issubclass(EligibilityView, TemplateView))
        self.assertTrue(issubclass(EligibilityView, PermissionRequiredMixin))
        self.assertEqual(EligibilityView.permission_required,
                         ('application.view_application', ))
