import json
from django.test import TestCase
from django.views import View
from application.presentation.views import (
    DraftUserDataView)


class DraftUserDataViewTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            'email_address': 'test@gmail.com',
            'age': 21
        }

    def test_view_properties(self):
        self.assertTrue(issubclass(DraftUserDataView, View))

    def send_successful_ajax_post(self, data):
        response = self.client.post(
            '/applications/application/draft/',
            data,
            follow=True,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        return response

    def test_sets_draft_user_data_to_session_on_post(self):
        response = self.send_successful_ajax_post(self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session['application_form_draft']['email_address'],
            self.data['email_address'])
        self.assertEqual(
            self.client.session['application_form_draft']['age'],
            str(self.data['age']))

    def test_sets_updates_draft_user_data_if_new_data(self):
        response = self.send_successful_ajax_post(self.data)
        self.assertEqual(response.status_code, 201)
        new_data = {
            'full_name': 'Jane Doe'
        }
        response = self.send_successful_ajax_post(new_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session['application_form_draft']['email_address'],
            self.data['email_address'])
        self.assertEqual(
            self.client.session['application_form_draft']['age'],
            str(self.data['age']))
        self.assertEqual(
            self.client.session['application_form_draft']['full_name'],
            'Jane Doe')

    def tests_returns_404_if_request_not_ajax(self):
        response = self.client.post(
            '/applications/application/draft/',
            self.data,
            follow=True,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode('utf-8'), "Not found")
