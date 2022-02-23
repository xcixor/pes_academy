from django.core import mail
from django.contrib.auth import get_user_model
from organization_subscription.tests.common import OrganizationSubscriptionBaseTestCase
from organization_subscription.presentation.views import (
    GetInitiateOrganizationSubscriptionView,
    PostInitiateOrganizationSubscriptionView)
from organization_subscription.forms import InitiateSubscriptionForm


User = get_user_model()


class InitiateOrganizationSubscriptionViewTestCase(OrganizationSubscriptionBaseTestCase):

    def setUp(self):
        super(InitiateOrganizationSubscriptionViewTestCase, self).setUp()
        self.form = {
            'subscriber_email': 'test@gmail.com',
        }

    def test_get_initiate_organization_subscription_view_properties(self):
        self.assertEqual(
            GetInitiateOrganizationSubscriptionView.template_name,
            'organization_subscription/initiate.html')

    def test_get_view_returns_200_OK(self):
        response = self.client.get('/organization-subscription/initiate/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_sets_form_in_context(self):
        response = self.client.get('/organization-subscription/initiate/')
        self.assertTrue(response.context['form'])

    def test_post_initiate_organization_subscription_view_properties(self):
        self.assertEqual(
            PostInitiateOrganizationSubscriptionView.template_name,
            'organization_subscription/initiate.html')
        self.assertEqual(
            PostInitiateOrganizationSubscriptionView.success_url,
            '/organization-subscription/initiate/')
        self.assertEqual(
            PostInitiateOrganizationSubscriptionView.form_class,
            InitiateSubscriptionForm)

    def test_on_post_creates_user(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(
            '/organization-subscription/initiate/',
            self.form, follow=True)
        self.assertRedirects(
            response, '/organization-subscription/initiate/', 302)
        self.assertEqual(User.objects.count(), 1)

    def test_on_post_sends_email(self):
        self.client.post(
            '/organization-subscription/initiate/',
            self.form, follow=True)
        self.assertEqual(len(mail.outbox), 1)