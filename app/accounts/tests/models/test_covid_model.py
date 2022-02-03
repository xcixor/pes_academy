from django.db import models
from accounts.tests.common import AccountsBaseTestCase
from accounts.models import BusinessOrganization


class CovidImpactTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(CovidImpactTestCase, self).setUp()
        self.impact = self.create_covid_impact()

    def test_has_relation_to_user_model(self):
        model = self.impact._meta.get_field('business').related_model
        self.assertEqual(model, BusinessOrganization)

    def test_user_fk_related_name(self):
        related = self.impact._meta.get_field(
            'business').remote_field.related_name
        self.assertEqual(related, 'covid_impact')

    def test_relation_to_user_model_is_one_to_one(self):
        relation = self.impact._meta.get_field('business')
        self.assertEqual(type(relation), models.OneToOneField)

    def test_user_relationship_on_delete_cascades(self):
        on_delete = self.impact._meta.get_field(
            'business').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_impact_one_properties(self):
        field = self.impact._meta.get_field('impact')
        self.assertIsInstance(field, models.TextField)
