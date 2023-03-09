from django.urls import reverse, resolve
from academy.tests.common import AcademyBaseTestCase
from academy.presentation.views import SessionDetails


class SessionDetailsTestCase(AcademyBaseTestCase):

    def setUp(self):
        super(SessionDetailsTestCase, self).setUp()
        self.session = self.create_session()

    def test_successfully_gets_session_details_page(self):
        url = reverse('academy:session_details', args=[self.session.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/session_details.html')

    def test_url_resolves(self):
        url = reverse('academy:session_details', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, SessionDetails)
