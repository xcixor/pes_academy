from django.db import models
from application.models.call_to_action import CallToAction
from application.tests.common import ApplicationBaseTestCase
from accounts.tests.common import User


class ApplicationModelTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(ApplicationModelTestCase, self).setUp()
        self.application = self.create_application_instance()

    def test_application_creator_properties(self):
        field = self.application._meta.get_field('application_creator')
        self.assertTrue(isinstance(field, models.OneToOneField))
        self.assertEqual(field.remote_field.related_name, 'application')
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.related_model, User)

    def test_call_to_action_properties(self):
        field = self.application._meta.get_field('call_to_action')
        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.remote_field.related_name, 'applications')
        self.assertEqual(field.remote_field.on_delete, models.SET_NULL)
        self.assertEqual(field.related_model, CallToAction)
        self.assertTrue(field.null)

    def test_status_field_properties(self):
        field = self.application._meta.get_field('status')
        self.assertEqual(field.default, 'step_one')
        self.assertEqual(field.max_length, 100)

    def test_slug_properties(self):
        field = self.application._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)
        self.assertEqual(
            field.help_text,
            'Unique text to append to the address for the application.')

    def test_sets_slug_on_save(self):
        print(self.application.slug)
        self.assertTrue(self.application.slug)