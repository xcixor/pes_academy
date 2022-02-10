from django.views.generic import TemplateView
from application.presentation.views  import SubmitView
from django.test import TestCase


class SubmitViewTestCase(TestCase):

    def setUp(self):
        super(SubmitViewTestCase, self).setUp()

    def test_view_properties(self):
        self.assertEqual(SubmitView.template_name, 'submit.html')
        self.assertTrue(issubclass(SubmitView, TemplateView))

    def test_successfully_gets_submit_page(self):
        response = self.client.get('/applications/submit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit.html')
