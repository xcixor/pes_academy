from django.views.generic import TemplateView
from accounts.presentation.views import ActivationEmailSentView
from django.test import TestCase


class ActivationEmailSentViewTestCase(TestCase):

    def setUp(self):
        super(ActivationEmailSentViewTestCase, self).setUp()

    def test_view_properties(self):
        self.assertEqual(
            ActivationEmailSentView.template_name,
            'registration/activation_email_sent.html')
        self.assertTrue(issubclass(ActivationEmailSentView, TemplateView))

    def test_successfully_gets_help_page(self):
        response = self.client.get('/accounts/activation-email-sent/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/activation_email_sent.html')
