import os
from django.views.generic import ListView
from application.models.call_to_action import CallToAction
from application.presentation.views import IndexView
from application.tests.common import ApplicationBaseTestCase


class IndexViewTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(IndexViewTestCase, self).setUp()
        self.application = self.create_call_to_action_instance()

    def test_view_properties(self):
        self.assertEqual(IndexView.template_name, 'index/index.html')
        self.assertTrue(issubclass(IndexView, ListView))
        self.assertEqual(IndexView.context_object_name, 'calls_to_action')
        self.assertEqual(IndexView.model, CallToAction)

    def test_successfully_gets_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_tagline_rendered_in_page(self):
        response = self.client.get('/')
        self.assertIn(self.application.tagline, response.content.decode())

    def test_image_rendered_in_page(self):
        filename = os.path.basename(self.application.image.name)
        filename = os.path.splitext(
            filename)[0] + os.path.splitext(filename)[1]
        response = self.client.get('/')
        self.assertTrue(filename in response.content.decode())
