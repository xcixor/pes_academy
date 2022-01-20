from django.views.generic import ListView
from sme.presentation.views import IndexView
from sme.models import Application
from sme.tests.common import SMETestCase


class IndexViewTestCase(SMETestCase):

    def setUp(self):
        super(IndexViewTestCase, self).setUp()
        self.application = self.create_application_instance()

    def test_view_properties(self):
        self.assertEqual(IndexView.template_name, 'index/index.html')
        self.assertTrue(issubclass(IndexView, ListView))
        self.assertEqual(IndexView.context_object_name, 'applications')
        self.assertEqual(IndexView.model, Application)

    def test_successfully_gets_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_tagline_rendered_in_page(self):
        response = self.client.get('/')
        self.assertInHTML(self.application.tagline, response.content.decode())

    def test_image_rendered_in_page(self):
        response = self.client.get('/')
        self.assertTrue(
            str(self.application.image) in response.content.decode())
