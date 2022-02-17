from organization_subscription.forms import InitiateSubscriptionForm
from organization_subscription.tests.common import OrganizationSubscriptionBaseTestCase


class EditJobFormTestCase(OrganizationSubscriptionBaseTestCase):

    def setUp(self):
        super(EditJobFormTestCase, self).setUp()
        data = {
            'subscriber_email': 'test@gmail.com',
        }
        self.form = InitiateSubscriptionForm(data)

    def test_has_expected_properties(self):
        fields = ['subscriber_email']
        self.assertEqual([*self.form.fields.keys()], fields)

    def test_validates_valid_form(self):
        self.assertTrue(self.form.is_valid())
        self.assertFalse(InitiateSubscriptionForm(
            {'subscriber_email': 'test'}).is_valid())
        self.assertFalse(InitiateSubscriptionForm(
            {'subscriber_email': ''}).is_valid())
