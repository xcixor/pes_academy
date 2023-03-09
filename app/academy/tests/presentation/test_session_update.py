from django.urls import reverse, resolve
from academy.tests.common import AcademyBaseTestCase
from academy.presentation.views import SessionUpdate
from academy.models import Session


class SessionUpdateTestCase(AcademyBaseTestCase):

    def setUp(self):
        super(SessionUpdateTestCase, self).setUp()
        self.session = self.create_session()

    def test_successfully_gets_session_update_page(self):
        url = reverse('academy:session_update', args=[self.session.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/session_details.html')

    def test_url_resolves(self):
        url = reverse('academy:session_update', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, SessionUpdate)

    def test_updates_session_details(self):
        self.assertEqual(Session.objects.get(
            pk=self.session.pk).title, self.session.title)
        url = reverse('academy:session_update', args=[self.session.pk])
        data = {
            'title': 'Introduction to Session'
        }
        self.client.post(url, data=data)
        self.assertNotEqual(Session.objects.get(
            pk=self.session.pk).title, self.session.title)
        self.assertEqual(Session.objects.get(
            pk=self.session.pk).title, data['title'])
