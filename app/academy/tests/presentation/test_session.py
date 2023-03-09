from django.test import TestCase
from django.urls import reverse, resolve
from academy.presentation.views import SessionView


class session_createTestCase(TestCase):

    def test_successfully_gets_session_create_page(self):
        url = reverse('academy:session_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/session.html')

    def test_url_resolves(self):
        url = reverse('academy:session_create')
        self.assertEqual(resolve(url).func.view_class, SessionView)
