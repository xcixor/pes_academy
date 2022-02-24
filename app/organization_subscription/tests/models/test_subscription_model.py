from django.db import models
from organization_subscription.tests.common import OrganizationSubscriptionBaseTestCase
from organization_subscription.models import OrganizationSubscription


class SubscriptionTestCase(OrganizationSubscriptionBaseTestCase):

    def setUp(self):
        super(SubscriptionTestCase, self).setUp()
        self.subscription = self.create_subscription()

    def test_subscriber_email_properties(self):
        field = self.subscription._meta.get_field('subscriber_email')
        self.assertTrue(isinstance(field, models.EmailField))
        self.assertTrue(field.unique)

    def test_subscription_properties(self):
        field = self.subscription._meta.get_field('subscription')
        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.remote_field.related_name, 'subscriptions')
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.related_model, OrganizationSubscription)
