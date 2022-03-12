from django.views.generic import TemplateView
from accounts.presentation.views import HelpView
from django.test import TestCase


class HelpViewTestCase(TestCase):

    def setUp(self):
        super(HelpViewTestCase, self).setUp()

    def test_view_properties(self):
        self.assertEqual(HelpView.template_name, 'help.html')
        self.assertTrue(issubclass(HelpView, TemplateView))

    def test_successfully_gets_help_page(self):
        response = self.client.get('/accounts/help/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help.html')
