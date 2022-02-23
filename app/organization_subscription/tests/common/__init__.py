from django.contrib.auth import get_user_model
from accounts.tests.common import AccountsBaseTestCase
from organization_subscription.models import OrganizationSubscription


User = get_user_model()


class OrganizationSubscriptionBaseTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(OrganizationSubscriptionBaseTestCase, self).setUp()

    def create_organization_subscription(self):
        subscription = OrganizationSubscription.objects.create(
            subscription_creator=self.create_user(),
            organization_subscriber=self.create_subscriber()
        )
        return subscription

    def create_subscriber(self):
        subscriber = User.objects.create(
            email='badi@gmail.com',
            age=46,
            gender='male',
            preferred_language='english',
            full_name='Tim Badi Mallo',
            username='bad_mallo',
            is_active=True
        )
        return subscriber