from django.views import View
from organization_subscription.tests.common import OrganizationSubscriptionBaseTestCase
from organization_subscription.presentation.views import ActivateSubscriptionView


class ActivateSubscriptionViewTestCase(OrganizationSubscriptionBaseTestCase):

    def test_view_properties(self):
        self.assertTrue(issubclass(ActivateSubscriptionView, View))

    def test_successful_activation_redirects_to_registration(self):
        pass

    def test_activation_failure_redirects_to_error_page(self):
        pass
