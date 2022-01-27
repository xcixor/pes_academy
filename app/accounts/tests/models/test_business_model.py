from django.db import models
from django.contrib.auth import get_user_model
from accounts.tests.common import AccountsBaseTestCase


User = get_user_model()


class BusinessModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(BusinessModelTestCase, self).setUp()
        self.business = self.create_business()

    def test_has_relation_to_user_model(self):
        model = self.business._meta.get_field('owner').related_model
        self.assertEqual(model, User)

    def test_user_fk_related_name(self):
        related = self.business._meta.get_field(
            'owner').remote_field.related_name
        self.assertEqual(related, 'business')

    def test_relation_to_user_model_is_one_to_one(self):
        relation = self.business._meta.get_field('owner')
        self.assertEqual(type(relation), models.OneToOneField)

    def test_user_relationship_on_delete_cascades(self):
        on_delete = self.business._meta.get_field(
            'owner').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_name_properties(self):
        field = self.business._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_facebook_link_properties(self):
        field = self.business._meta.get_field('facebook_link')
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.null)

    def test_twitter_link_properties(self):
        field = self.business._meta.get_field('twitter_link')
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.null)

    def test_linkedin_link_properties(self):
        field = self.business._meta.get_field('linkedin_link')
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.null)

    def test_instagram_link_properties(self):
        field = self.business._meta.get_field('instagram_link')
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.null)

    def test_whatsapp_business_link_properties(self):
        field = self.business._meta.get_field('instagram_link')
        self.assertIsInstance(field, models.URLField)
        self.assertEqual(field.max_length, 200)
        self.assertTrue(field.null)

    def test_value_chain_properties(self):
        field = self.business._meta.get_field('value_chain')
        self.assertIsInstance(field, models.CharField)
        CHOICES = [
            ('chain_one', 'Primary production (farming)'),
            ('chain_two', 'Input supplier'),
            ('chain_three', 'Processor (value addition)'),
            ('chain_four', 'Aggregator'), ('chain_five', 'Distributor'),
            ('chain_six', 'Retailer'), ('chain_seven', 'Service provider')]
        self.assertEqual(field.choices, CHOICES)

    def test_existence_period_properties(self):
        field = self.business._meta.get_field('existence_period')
        self.assertIsInstance(field, models.CharField)
        CHOICES = [
            ('period_one', 'Below 1 year'),
            ('period_two', 'More than 1 year but less than 2 years'),
            ('period_three', 'Between 2 to 5 years'),
            ('period_four', 'Over 5 years')]
        self.assertEqual(field.choices, CHOICES)

    def test_stage_properties(self):
        field = self.business._meta.get_field('stage')
        self.assertIsInstance(field, models.CharField)
        CHOICES = [
            ('stage_one', 'Product or service is still being developed'),
            ('stage_two', 'Product or service is at MVP stage. Currently piloting with target users'),
            ('stage_three', 'Product or service has been availed in the market. There are no sales or revenues as yet'),
            ('stage_four', 'Product or service is in the market. There are sales/revenues')]
        self.assertEqual(field.choices, CHOICES)

    def test_returns_useful_name(self):
        self.assertEqual(str(self.business), 'Caravan Tech')