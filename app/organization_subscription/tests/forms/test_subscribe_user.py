from django.core import mail
from django import forms
from organization_subscription.forms import InitiateSubscriptionForm
from organization_subscription.tests.common import (
    OrganizationSubscriptionBaseTestCase)
from common.utils.tests import RequestFactoryMixin


class EditJobFormTestCase(OrganizationSubscriptionBaseTestCase, RequestFactoryMixin):

    def setUp(self):
        super(EditJobFormTestCase, self).setUp()
        self.data = {
            'subscriber_email': 'test@gmail.com',
        }
        self.form = InitiateSubscriptionForm(self.data)
        self.request = self.generate_request()

    def test_has_expected_properties(self):
        fields = ['subscriber_email']
        self.assertEqual([*self.form.fields.keys()], fields)

    def test_validates_valid_form(self):
        self.assertTrue(self.form.is_valid())
        self.assertFalse(InitiateSubscriptionForm(
            {'subscriber_email': 'test'}).is_valid())
        self.assertFalse(InitiateSubscriptionForm(
            {'subscriber_email': ''}).is_valid())

    def test_can_send_email_to_join_organization_channel(self):
        self.assertTrue(self.form.is_valid())
        self.form.send_subscription_email(self.user.email, self.request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Join Our Organization Channel')
        to_email = self.data['subscriber_email']
        self.assertEqual(mail.outbox[0].to[0], to_email)

    def test_can_create_subscription(self):
        self.assertTrue(self.form.is_valid())
        organization_subscription = self.create_organization_subscription()
        subscription = self.form.subscribe_user(organization_subscription)
        self.assertTrue(subscription)

    def test_raises_error_if_subscription_exists(self):
        self.assertTrue(self.form.is_valid())
        organization_subscription = self.create_organization_subscription()
        self.form.subscribe_user(organization_subscription)
        with self.assertRaises(forms.ValidationError) as ve:
            self.form.subscribe_user(organization_subscription)
