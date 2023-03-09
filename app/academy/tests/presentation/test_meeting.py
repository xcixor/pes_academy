from academy.tests.common import AcademyBaseTestCase
from django.urls import reverse, resolve
from academy.presentation.views import (
    SetupMeetingView, GetSetupMeetingPageView)
from academy.models import Meeting


class MeetingTestCase(AcademyBaseTestCase):

    def setUp(self) -> None:
        super(MeetingTestCase, self).setUp()
        self.session = self.create_session()

    def test_successfully_gets_meeting_setup_page(self):
        url = reverse('academy:meeting_setup', args=[self.session.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/meeting_setup.html')

    def test_get_create_meeting_url_resolves(self):
        url = reverse('academy:meeting_setup', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, GetSetupMeetingPageView)

    def test_post_meeting_url_resolves(self):
        url = reverse('academy:meeting_create', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, SetupMeetingView)

    def test_creates_meeting_on_post(self):
        self.assertEqual(Meeting.objects.count(), 0)
        url = reverse('academy:meeting_create', args=[self.session.pk])
        data = {
            'session': self.session.pk,
            'link': 'https://calendly.com/test_calender/introduction-to-marketing',
        }
        res = self.client.post(url, data)
        redirect_url = reverse(
            'academy:session_details',
            args=[self.session.pk])
        self.assertEqual(Meeting.objects.count(), 1)
        self.assertRedirects(res, redirect_url, 302)
