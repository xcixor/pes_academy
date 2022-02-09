from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.test import TestCase
from accounts.presentation.views import UserLoginView


class LoginTestCase(TestCase):

    def setUp(self):
        user_model = get_user_model()
        user = user_model.objects._create_user(
            'test', 'mozzart1800@')
        self.user = user
        self.form = {
            'username': 'test',
            'password': 'mozzart1800@'
        }

    def test_view_properties(self):
        self.assertTrue(issubclass(UserLoginView, LoginView))
        self.assertEqual(UserLoginView.template_name, 'registration/login.html')
    def test_login_redirects_to_the_next_page(self):
        response = self.client.post(
            '/accounts/login/?next=/', self.form, follow=True)
        self.assertRedirects(response, '/', 302)

    def test_adds_success_message(self):
        response = self.client.post(
            '/accounts/login/?next=/', self.form, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'Welcome back test!')
        self.assertEqual(message.tags, 'success')
        self.assertEqual(message.message, expected_message)
