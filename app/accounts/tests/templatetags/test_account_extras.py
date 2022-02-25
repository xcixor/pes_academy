from accounts.tests.common import AccountsBaseTestCase
from accounts.templatetags.account_extras import (
    get_profile, get_application_url)
from organization_subscription.models import (
    Subscription, OrganizationSubscription)


class AccountExtrasTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(AccountExtrasTestCase, self).setUp()

    def test_can_get_profile(self):
        self.assertTrue(get_profile(self.user.email))

    def test_can_get_application_url(self):
        self.create_application()
        subscription = OrganizationSubscription.objects.create(
            subscription_creator=self.user)
        Subscription.objects.create(
            subscriber_email=self.user.email, subscription=subscription)
        self.assertTrue(get_application_url(self.user.email))
