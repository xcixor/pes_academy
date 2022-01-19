from django.test import TestCase
from django.views.generic import TemplateView
from sme.presentation.views import IndexView


class IndexViewTestCase(TestCase):

    def test_view_properties(self):
        self.assertEqual(IndexView.template_name, 'index/index.html')
        self.assertTrue(issubclass(IndexView, TemplateView))

    def test_successfully_gets_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')
