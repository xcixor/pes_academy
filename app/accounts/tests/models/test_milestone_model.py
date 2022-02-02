from django.db import models
from accounts.tests.common import AccountsBaseTestCase
from accounts.models import BusinessOrganization


class MilestoneModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(MilestoneModelTestCase, self).setUp()
        self.milestone = self.create_milestone()

    def test_has_relation_to_user_model(self):
        model = self.milestone._meta.get_field('businesses').related_model
        self.assertEqual(model, BusinessOrganization)

    def test_user_fk_related_name(self):
        related = self.milestone._meta.get_field(
            'businesses').remote_field.related_name
        self.assertEqual(related, 'businesses')

    def test_relation_to_user_model_is_one_to_one(self):
        relation = self.milestone._meta.get_field('businesses')
        self.assertEqual(type(relation), models.ManyToManyField)

    def test_user_relationship_on_delete_cascades(self):
        blank = self.milestone._meta.get_field('businesses').blank
        self.assertTrue(blank)

    def test_milestone_properties(self):
        field = self.milestone._meta.get_field('milestone')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_returns_human_readable_form(self):
        self.assertEqual(str(self.milestone), 'Revenue Growth')
