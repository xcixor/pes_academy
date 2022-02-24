from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.presentation.views import DashboardView
from accounts.tests.common import AccountsBaseTestCase


class DashboardViewTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(DashboardViewTestCase, self).setUp()

    def login_user(self):
        self.client.login(
            username=self.user.username, password='socrates123@')

    def test_view_properties(self):
        self.assertEqual(
            DashboardView.template_name, 'profile/dashboard.html')
        self.assertTrue(issubclass(DashboardView, TemplateView))
        self.assertTrue(issubclass(DashboardView, LoginRequiredMixin))

    def test_successfully_gets_submit_page(self):
        self.login_user()
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/dashboard.html')
