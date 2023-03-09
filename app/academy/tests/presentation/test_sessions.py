from django.test import TestCase
from django.urls import reverse, resolve
from academy.presentation.views import SessionsView


class sessionsTestCase(TestCase):

    def test_successfully_gets_sessions_page(self):
        url = reverse('academy:sessions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/sessions.html')

    def test_url_resolves(self):
        url = reverse('academy:sessions')
        self.assertEqual(resolve(url).func.view_class, SessionsView)
