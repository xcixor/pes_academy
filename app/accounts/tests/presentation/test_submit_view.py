from django.views.generic import TemplateView
from accounts.presentation.views  import SubmitView
from django.test import TestCase
from django.views import View

class SubmitViewTestCase(TestCase):

    def setUp(self):
        super(SubmitViewTestCase, self).setUp()
        
    def test_view_properties(self):
        self.assertEqual(SubmitView.template_name, 'submit.html')
        self.assertTrue(issubclass(SubmitView, TemplateView))

    def test_successfully_gets_submit_page(self):
        response = self.client.get('/accounts/submit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit.html')
