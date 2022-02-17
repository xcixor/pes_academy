from django.db import models
from organization_subscription.tests.common import OrganizationSubscriptionBaseTestCase


class OrganizationSubscriptionTestCase(OrganizationSubscriptionBaseTestCase):

    def setUp(self):
        super(OrganizationSubscriptionBaseTestCase, self).setUp()
        self.subscription = self.create_organization_subscription()

    def test_has_organization_subscription_id_property(self):
        self.assertTrue(
            hasattr(self.subscription,
                    'organization_subscription_id'))
        self.assertEqual(
            self.subscription.organization_subscription_id,
            f'BUS-{self.subscription.id}')

    def test_has_subscription_creator_field(self):
        field = self.subscription._meta.get_field('subscription_creator')
        self.assertEqual(field.remote_field.related_name, 'organization_admin')
        self.assertIsInstance(field, models.OneToOneField)

    def test_user_relationship_on_delete_cascades(self):
        on_delete = self.subscription._meta.get_field(
            'subscription_creator').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_has_subscriber_field(self):
        field = self.subscription._meta.get_field('organization_subscriber')
        self.assertEqual(field.remote_field.related_name, 'organization_subscribers')
        self.assertIsInstance(field, models.ForeignKey)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_subscriber_relationship_on_delete_sets_null(self):
        on_delete = self.subscription._meta.get_field(
            'organization_subscriber').remote_field.on_delete
        self.assertEqual(on_delete, models.SET_NULL)

    def test_has_organization_field(self):
        field = self.subscription._meta.get_field('organization')
        self.assertEqual(field.remote_field.related_name, 'organization')
        self.assertIsInstance(field, models.OneToOneField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_organization_relationship_on_delete_sets_null(self):
        on_delete = self.subscription._meta.get_field(
            'organization').remote_field.on_delete
        self.assertEqual(on_delete, models.SET_NULL)

    def test_defines_human_readable_name(self):
        self.assertEqual(
            str(self.subscription),
            self.subscription.organization_subscription_id)
