from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django_redis import get_redis_connection
from accounts.tests.common import AccountsBaseTestCase
from application.presentation.views import (
    DraftApplicationDataView)
from application.services import get_draft_application_data_from_cache


class DraftApplicationDataViewTestCase(AccountsBaseTestCase):

    def setUp(self) -> None:
        super(DraftApplicationDataViewTestCase, self).setUp()
        self.data = {
            'milestones': 'Many',
            'organization_name': "Private Equity Support"
        }
        self.application = self.create_application()

    def tearDown(self) -> None:
        get_redis_connection("default").flushall()

    def test_view_properties(self):
        self.assertTrue(issubclass(DraftApplicationDataView, View))
        self.assertTrue(issubclass(
            DraftApplicationDataView, LoginRequiredMixin))

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
            self.client.session['application_form_draft']['milestones'],
            self.data['milestones'])
        self.assertEqual(
            self.client.session['application_form_draft']['organization_name'],
            str(self.data['organization_name']))

    def test_sets_updates_draft_user_data_if_new_data(self):
        self.login_user()
        response = self.send_successful_ajax_post(self.data)
        self.assertEqual(response.status_code, 201)
        new_data = {
            'facebook_link': 'Jane Doe'
        }
        response = self.send_successful_ajax_post(new_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session['application_form_draft']['milestones'],
            self.data['milestones'])
        self.assertEqual(
            self.client.session['application_form_draft']['organization_name'],
            str(self.data['organization_name']))
        self.assertEqual(
            self.client.session['application_form_draft']['facebook_link'],
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
            'facebook_link': 'Jane Doe'
        }
        self.send_successful_ajax_post(new_data)
        data = get_draft_application_data_from_cache(self.application.id)
        self.assertEqual(data['facebook_link'], 'Jane Doe')
