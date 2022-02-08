from django.test import TestCase
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView, FormView
from accounts.presentation.views import (
    GetRegistrationView, PostRegistrationView, RegistrationView)
from accounts.forms import RegistrationForm


User = get_user_model()


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.form = {
            'email': 'test@gmail.com',
            'password1': 'test1234*',
            'password2': 'test1234*',
            'username': 'pish_dush'
        }

    def test_post_registration_view(self):

        self.assertTrue(issubclass(PostRegistrationView, FormView))
        self.assertEqual(
            PostRegistrationView.form_class,
            RegistrationForm)
        self.assertEqual(
            PostRegistrationView.template_name,
            'registration/registration.html')
        self.assertEqual(PostRegistrationView.success_url, '/accounts/submit/')

    def test_get_registration_view(self):
        self.assertEqual(
            GetRegistrationView.template_name,
            'registration/registration.html')
        self.assertTrue(issubclass(GetRegistrationView, TemplateView))

    def test_main_registration_view(self):
        self.assertTrue(issubclass(RegistrationView, View))

    def test_redirects_on_successful_registration(self):
        registration_request = self.client.post(
            '/accounts/register/', self.form, follow=True)
        self.assertRedirects(registration_request, '/accounts/submit/', 302)

    def test_user_saved_on_successful_registration(self):
        self.client.post(
            '/accounts/register/', self.form, follow=True)
        saved_user = User.objects.get(email=self.form['email'])
        self.assertEqual(saved_user.username, self.form['username'])

    def test_get_user_registration_page(self):
        get_response = self.client.get('/accounts/register/')
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(
            get_response, 'registration/registration.html')
        self.assertEqual(
            get_response.context['form'], RegistrationForm)

    def test_on_form_invalid_sets_form_name_correctly(self):
        self.form['password2'] = 'notlikepass1'
        registration_request = self.client.post(
            '/accounts/register/', self.form)
        self.assertIsInstance(
            registration_request.context['form'],
            RegistrationForm)

    def test_on_form_invalid_returns_registration_template_if_not_htmx(self):
        self.form['password2'] = 'notlikepass1'
        registration_request = self.client.post(
            '/accounts/register/', self.form)
        self.assertTemplateUsed(registration_request,
                                'registration/registration.html')

    def test_sets_form_data_in_session_if_form_invalid(self):
        self.form['password2'] = 'notlikepass1'
        self.client.post(
            '/accounts/register/', self.form)
        self.assertEqual(self.client.session.get('registration_details')[
                         'username'], self.form['username'])
        self.assertTrue(self.client.session.get('registration_details'))

    def test_does_not_set_passwords_in_session_if_form_invalid(self):
        self.form['password2'] = 'notlikepass1'
        self.client.post(
            '/accounts/register/', self.form)
        with self.assertRaises(KeyError):
            self.assertFalse(self.client.session.get(
                'registration_details')['password1'])
            self.assertFalse(self.client.session.get(
                'registration_details')['password2'])

    def test_removes_saved_registration_details_if_form_valid(self):
        self.form['password2'] = 'notlikepass1'
        self.client.post(
            '/accounts/register/', self.form)
        self.assertTrue(self.client.session.get('registration_details'))
        self.form['password2'] = 'test1234*'
        self.client.post(
            '/accounts/register/', self.form)
        self.assertFalse(self.client.session.get('registration_details'))