from django.contrib.auth import get_user_model
from accounts.tests.common import AccountsBaseTestCase
from common.utils.common_queries import get_application
from organization_subscription.models import (
    OrganizationSubscription, Subscription)
from application.models import Application


class GetApplicationTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(GetApplicationTestCase, self).setUp()

    def test_can_get_application_if_user_application_creator(self):
        self.application = self.create_application()
        application, msg = get_application(self.user)
        self.assertTrue(application)
        self.assertIsNone(msg)

    def test_can_get_application_if_user_is_subscriber(self):
        user = get_user_model().objects._create_user(
            'admin_user', 'socrates123@')
        call_to_action = self.create_call_to_action_instance()
        application = Application.objects.create(
            application_creator=user,
            call_to_action=call_to_action,
            slug=call_to_action.slug
        )
        application, msg = get_application(self.user)
        self.assertIsNone(application)

        organization_subscription = OrganizationSubscription.objects.create(
            subscription_creator=user
        )
        Subscription.objects.create(
            subscriber_email=self.user.email,
            subscription=organization_subscription
        )
        application, msg = get_application(self.user)
        self.assertIsNotNone(application)
