from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django_redis import get_redis_connection
from accounts.tests.common import AccountsBaseTestCase
from application.presentation.views import (
    DraftUserDataView)
from application.services import get_draft_application_data_from_redis_cache


class DraftUserDataViewTestCase(AccountsBaseTestCase):

    def setUp(self) -> None:
        super(DraftUserDataViewTestCase, self).setUp()
        self.data = {
            'email_address': 'test@gmail.com',
            'age': 21
        }
        self.application = self.create_application()

    def tearDown(self) -> None:
        get_redis_connection("default").flushall()

    def test_view_properties(self):
        self.assertTrue(issubclass(DraftUserDataView, View))
        self.assertTrue(issubclass(DraftUserDataView, LoginRequiredMixin))

    def login_user(self):
        self.client.login(
            username=self.user.username, password='socrates123@')

    def send_successful_ajax_post(self, data):
        self.login_user()
        response = self.client.post(
            '/applications/application/draft/',
            data,
            follow=True,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        return response

    def test_sets_draft_user_data_to_session_on_post(self):
        self.login_user()
        response = self.send_successful_ajax_post(self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session['application_form_draft']['email_address'],
            self.data['email_address'])
        self.assertEqual(
            self.client.session['application_form_draft']['age'],
            str(self.data['age']))

    def test_sets_updates_draft_user_data_if_new_data(self):
        self.login_user()
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
        self.login_user()
        response = self.client.post(
            '/applications/application/draft/',
            self.data,
            follow=True,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode('utf-8'), "Not found")

    def test_sets_data_in_redis_cache(self):
        self.login_user()
        new_data = {
            'full_name': 'Jane Doe'
        }
        self.send_successful_ajax_post(new_data)
        data = get_draft_application_data_from_redis_cache(self.application.id)
        self.assertEqual(data['full_name'], 'Jane Doe')
