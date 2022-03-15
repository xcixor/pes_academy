from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from application.presentation.views import (
    PostApplicationDocumentFormView, JsonableResponseMixin)
from application.tests.common import ApplicationBaseTestCase
from application.forms import ApplicationDocumentForm
from application.models import ApplicationDocument


class PostApplicationDocumentFormViewTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(PostApplicationDocumentFormViewTestCase, self).setUp()
        self.application = self.create_application_instance()
        self.user = self.application.application_creator
        self.data = {
            'document_name': 'KRA Pin',
            'document': self.get_pdf(),
            'application': self.application.pk
        }

    def login_user(self):
        self.user.is_active = True
        self.user.save()
        self.client.login(
            username=self.user.username, password='socrates123@')

    def test_view_properties(self):
        self.assertTrue(issubclass(PostApplicationDocumentFormView, FormView))
        self.assertTrue(issubclass(
            PostApplicationDocumentFormView, LoginRequiredMixin))
        self.assertTrue(issubclass(
            PostApplicationDocumentFormView, JsonableResponseMixin))
        self.assertEqual(
            PostApplicationDocumentFormView.form_class,
            ApplicationDocumentForm)
        self.assertEqual(
            PostApplicationDocumentFormView.template_name,
            'application/application_form.html')

    def test_saves_document(self):
        self.login_user()
        self.assertEqual(ApplicationDocument.objects.count(), 0)
        response = self.client.post(
            '/applications/document/', self.data, follow=True)
        self.assertRedirects(
            response, f'/applications/{self.application.slug}/', 302)
        self.assertEqual(ApplicationDocument.objects.count(), 1)

    def test_can_save_document_with_ajax(self):
        self.login_user()
        self.assertEqual(ApplicationDocument.objects.count(), 0)
        response = self.client.post(
            '/applications/document/', self.data, follow=True,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',)
        self.assertEqual(ApplicationDocument.objects.count(), 1)
        self.assertEqual(response.status_code, 201)
