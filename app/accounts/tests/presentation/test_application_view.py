from django.views.generic import DetailView
from accounts.presentation.views.application import ApplicationView
from sme.models import Application
from sme.tests.common import SMETestCase


class ApplicationViewTestCase(SMETestCase):

    def setUp(self):
        super(ApplicationViewTestCase, self).setUp()
        self.application = self.create_application_instance()

    def test_view_properties(self):
        self.assertTrue(issubclass(ApplicationView, DetailView))
        self.assertEqual(ApplicationView.model, Application)
        self.assertEqual(ApplicationView.context_object_name, 'application')

    def test_gets_application_page_successfully(self):
        response = self.client.get(
            f'/accounts/applications/{self.application.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_form.html')
