from django.contrib.auth.views import LoginView
from accounts.tests.common import AccountsBaseTestCase
from accounts.presentation.views import UserLoginView


class LoginTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(LoginTestCase, self).setUp()
        self.form = {
            'username': 'normal_user',
            'password': 'socrates123@'
        }

    def test_view_properties(self):
        self.assertTrue(issubclass(UserLoginView, LoginView))
        self.assertEqual(UserLoginView.template_name,
                         'registration/login.html')

    def test_login_redirects_to_the_next_page(self):
        next_url = '/accounts/help/'
        response = self.client.post(
            f'/accounts/login/?next={next_url}', self.form, follow=True)
        self.assertRedirects(
            response, next_url, 302)

    def test_adds_success_message(self):
        url = '/accounts/help/'
        response = self.client.post(
            f'/accounts/login/?next={url}', self.form, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'Welcome back normal_user')
        self.assertEqual(message.tags, 'success')
        self.assertEqual(message.message, expected_message)
