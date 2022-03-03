from django.db import models
from application.models.application import Application
from application.tests.common import ApplicationBaseTestCase


class ApplicationDocumentTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(ApplicationDocumentTestCase, self).setUp()
        self.document = self.create_application_document()

    def test_name_properties(self):
        field = self.document._meta.get_field('document_name')
        self.assertEqual(field.max_length, 200)

    def test_application_foreign_key(self):
        field = self.document._meta.get_field('application')
        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.remote_field.related_name, 'documents')
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.related_model, Application)

    def test_stores_in_custom_folder(self):
        self.assertIn(
            f'applications/{self.document.application}/',
            str(self.document.document))

    def test_defines_user_readable_name(self):
        self.assertEqual(str(self.document), 'KRA Pin')
