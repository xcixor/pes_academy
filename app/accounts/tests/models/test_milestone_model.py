from django.db import models
from accounts.tests.common import AccountsBaseTestCase
from accounts.models import BusinessOrganization


class MilestoneModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(MilestoneModelTestCase, self).setUp()
        self.milestone = self.create_milestone()

    def test_has_relation_to_user_model(self):
        model = self.milestone._meta.get_field('business').related_model
        self.assertEqual(model, BusinessOrganization)

    def test_user_fk_related_name(self):
        related = self.milestone._meta.get_field(
            'business').remote_field.related_name
        self.assertEqual(related, 'milestones')

    def test_relation_to_user_model_is_one_to_one(self):
        relation = self.milestone._meta.get_field('business')
        self.assertEqual(type(relation), models.ForeignKey)

    def test_user_relationship_on_delete_cascades(self):
        on_delete = self.milestone._meta.get_field(
            'business').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_milestone_properties(self):
        field = self.milestone._meta.get_field('milestone')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
