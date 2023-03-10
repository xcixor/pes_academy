from academy.tests.common import AcademyBaseTestCase
from django.urls import reverse, resolve
from academy.presentation.views import UploadMaterialView
from academy.models import SessionMaterial
from django.core import mail


class UploadMaterialViewTestCase(AcademyBaseTestCase):

    def setUp(self) -> None:
        super(UploadMaterialViewTestCase, self).setUp()
        self.session = self.create_session()

    def test_view_properties(self):
        self.assertEqual(UploadMaterialView.template_name,
                         'staff/material.html')
        self.assertEqual(UploadMaterialView.model,
                         SessionMaterial)
        fields = ['material_name', 'material', 'session']
        self.assertEqual(UploadMaterialView.fields,
                         fields)

    def upload_material(self):
        url = reverse('academy:material_upload', args=[self.session.pk])
        data = {
            'material': self.get_pdf(),
            'material_name': 'Marketing Info',
            'session': self.session.pk
        }
        response = self.client.post(url, data)
        return response

    def test_upload_material(self):
        self.assertEqual(SessionMaterial.objects.count(), 0)
        response = self.upload_material()
        response.content.decode()
        self.assertEqual(SessionMaterial.objects.count(), 1)

    def test_upload_material_redirects(self):
        response = self.upload_material()
        url = reverse('academy:session_details', kwargs={
                      'pk': self.session.pk})
        self.assertRedirects(response, url, 302)

    def test_on_upload_success_material_email_sent(self):
        self.upload_material()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Hi, your coach uploaded a new material: ',
                      mail.outbox[0].alternatives[0][0])
        self.assertIn('Please login to your account to view it, thank you.',
                      mail.outbox[0].alternatives[0][0])

    def test_on_upload_success_sets_success_message(self):
        url = reverse('academy:material_upload', args=[self.session.pk])
        data = {
            'material': self.get_pdf(),
            'material_name': 'Marketing Info',
            'session': self.session.pk
        }
        response = self.client.post(url, data, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue(
            "Great! the material has been saved." in message.message)

    def test_on_upload_failure_sets_failure_message(self):
        url = reverse('academy:material_upload', args=[self.session.pk])
        data = {
            'material': '',
            'material_name': 'Marketing Info',
            'session': self.session.pk
        }
        response = self.client.post(url, data)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(
            "Hmm! something went wrong, please try again." in message.message)

    def test_on_upload_failure_returns_form_with_errors(self):
        url = reverse('academy:material_upload', args=[self.session.pk])
        data = {
            'material': '',
            'material_name': 'Marketing Info',
            'session': self.session.pk
        }
        response = self.client.post(url, data)
        self.assertIn("This field is required.", response.content.decode())
