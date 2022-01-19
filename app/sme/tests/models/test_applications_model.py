from django.db import models
from sme.tests.common import SMETestCase


class ApplicationModelTestCase(SMETestCase):

    def setUp(self):
        super(ApplicationModelTestCase, self).setUp()
        self.application = self.create_application_instance()

    def test_tagline_properties(self):
        field = self.application._meta.get_field('tagline')
        self.assertIsInstance(field, models.CharField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(field.max_length, 255)
        self.assertEqual(
            field.help_text, 'A title for the application.')

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

    def test_description_properties(self):
        field = self.application._meta.get_field('description')
        self.assertIsInstance(field, models.TextField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(
            field.help_text, 'A description of what the application is about.')

    def test_image_properties(self):
        field = self.application._meta.get_field('image')
        self.assertIsInstance(field, models.ImageField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEqual(
            field.help_text, 'An image to display in the applications page.')

    def test_material_field_upload_folder(self):
        self.assertIn(
            f'/media/applications/{self.application.slug}/',
            self.application.image.url)

    def tearDown(self):
        self.delete_test_images(
            f'/media/applications/{self.application.slug}/')
