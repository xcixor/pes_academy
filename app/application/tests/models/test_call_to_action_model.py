from django.db import models
from application.tests.common import ApplicationBaseTestCase


class ApplicationModelTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(ApplicationModelTestCase, self).setUp()
        self.call_to_action = self.create_call_to_action_instance()

    def test_tagline_properties(self):
        field = self.call_to_action._meta.get_field('tagline')
        self.assertIsInstance(field, models.CharField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(field.max_length, 255)
        self.assertEqual(
            field.help_text, 'A title for the call to action.')

    def test_slug_properties(self):
        field = self.call_to_action._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)
        self.assertEqual(
            field.help_text,
            'Unique text to append to the address for the call to action.')

    def test_description_properties(self):
        field = self.call_to_action._meta.get_field('description')
        self.assertIsInstance(field, models.TextField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(
            field.help_text, 'A description of what the call to action is about.')

    def test_image_properties(self):
        field = self.call_to_action._meta.get_field('image')
        self.assertIsInstance(field, models.ImageField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(
            field.help_text, 'An image to display in the call to action page.')

    def test_material_field_upload_folder(self):
        self.assertIn(
            f'/applications/{self.call_to_action.slug}/',
            self.call_to_action.image.url)

    def test_deadline_field_properties(self):
        field = self.call_to_action._meta.get_field('deadline')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(
            field.help_text, 'The call to action\'s deadline.')

    def test_created_field_properties(self):
        field = self.call_to_action._meta.get_field('created')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertFalse(field.null)
        self.assertTrue(field.auto_now_add)
        self.assertEqual(
            field.help_text, 'The date the call to action was created.')

    def test_updated_field_properties(self):
        field = self.call_to_action._meta.get_field('updated')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertFalse(field.null)
        self.assertTrue(field.auto_now)
        self.assertEqual(
            field.help_text, 'The date the call to action was updated.')

    def test_available_for_applications_field_properties(self):
        field = self.call_to_action._meta.get_field(
            'available_for_applications')
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.null)
        self.assertFalse(field.default)
        help_text = (
            'Designates whether applications can be made '
            'for this call to action. If checked it and is within the deadline, '
            'applicants can view it on the application page.'
        )
        self.assertEqual(
            field.help_text, help_text)

    def test_defines_a_human_readable_name(self):
        self.assertEqual(str(self.call_to_action), 'Call For Application 1')

    def tearDown(self):
        self.delete_test_images(
            f'/media/applications/{self.call_to_action.slug}/')