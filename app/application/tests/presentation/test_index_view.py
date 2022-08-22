from django.views.generic import ListView
from application.presentation.views import IndexView
from application.tests.common import ApplicationBaseTestCase


class IndexViewTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(IndexViewTestCase, self).setUp()
        self.application = self.create_call_to_action_instance()

    def test_view_properties(self):
        self.assertEqual(IndexView.template_name, 'index/index.html')
        self.assertTrue(issubclass(IndexView, ListView))

    def test_successfully_gets_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')
