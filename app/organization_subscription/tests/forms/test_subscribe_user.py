from django.core import mail
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
        user = self.create_user()
        self.form.send_subscription_email(user, self.request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Join Our Organization Channel')
        to_email = self.data['subscriber_email']
        self.assertEqual(mail.outbox[0].to[0], to_email)
