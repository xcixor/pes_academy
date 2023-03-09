from django.test import TestCase
from django.urls import reverse, resolve
from academy.presentation.views import CoacheesView


class CoacheesTestCase(TestCase):

    def test_successfully_gets_coachees_page(self):
        url = reverse('academy:coachees')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/coachees.html')

    def test_url_resolves(self):
        url = reverse('academy:coachees')
        self.assertEqual(resolve(url).func.view_class, CoacheesView)
