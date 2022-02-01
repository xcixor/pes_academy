from django.db import models
from accounts.tests.common import AccountsBaseTestCase
from accounts.models import BusinessOrganization


class MilestoneModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(MilestoneModelTestCase, self).setUp()
        self.milestone = self.create_milestone()

    def test_milestone_properties(self):
        field = self.milestone._meta.get_field('milestone')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_returns_human_readable_form(self):
        self.assertEqual(str(self.milestone), 'Revenue Growth')
