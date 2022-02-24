from django.contrib.auth import get_user_model
from accounts.tests.common import AccountsBaseTestCase
from organization_subscription.models import (
    OrganizationSubscription, Subscription)


User = get_user_model()


class OrganizationSubscriptionBaseTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(OrganizationSubscriptionBaseTestCase, self).setUp()

    def create_organization_subscription(self):
        subscription = OrganizationSubscription.objects.create(
            subscription_creator=self.user
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

    def create_subscription(self):
        subscription = Subscription.objects.create(
            subscriber_email='badi@gmail.com',
            subscription=self.create_organization_subscription()
        )
        return subscription