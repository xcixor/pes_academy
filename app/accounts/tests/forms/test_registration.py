from django.test import TestCase
from django import forms
from django.core import mail
from accounts.forms import RegistrationForm
from accounts.models import User
from common.utils.tests import RequestFactoryMixin


class RegistrationFormTestCase(TestCase, RequestFactoryMixin):

    def setUp(self):
        self.data = {
            'email': 'testuser@gmail.com',
            'password1': 'cli3ntnu1#',
            'password2': 'cli3ntnu1#',
            'username': 'pish_dush',
            'is_applying_for_a_call_to_action': True,
            'terms': True
        }
        self.form = RegistrationForm(self.data)
        self.request = self.generate_request()

    def test_specifies_model(self):
        self.assertIsInstance(self.form.Meta.model(), User)

    def test_defines_fields(self):
        self.assertTrue(self.form.fields['email'])
        self.assertTrue(self.form.fields['password1'])
        self.assertTrue(self.form.fields['password2'])

    def test_password_1_properties(self):
        self.assertIsInstance(
            self.form.fields['password1'].widget, forms.PasswordInput)

    def test_password_2_properties(self):
        self.assertIsInstance(
            self.form.fields['password2'].widget, forms.PasswordInput)

    def test_cleans_password(self):
        self.data['password2'] = 'NotTheSame'
        form = RegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'][0],
            'Please make sure your passwords match.')

    def test_validates_user_data(self):
        self.assertTrue(self.form.is_valid())

    def test_saves_user(self):
        self.assertTrue(self.form.is_valid())
        self.form.save(commit=True)
        saved_user = User.objects.get(email=self.data['email'])
        self.assertEqual(saved_user.username, self.data['username'])

    def test_saves_user_with_password(self):
        self.assertTrue(self.form.is_valid())
        self.form.save(commit=True)
        saved_user = User.objects.get(email=self.data['email'])
        self.assertTrue(saved_user.password)
        self.assertNotEqual(saved_user.password, self.data['password1'])

    def test_validates_user_password_not_too_common(self):
        data = self.data
        data['password1'] = 'password'
        data['password2'] = 'password'
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1']
                         [0], 'This password is too common.')

    def test_validates_user_password_not_less_than_eight_characters(self):
        data = self.data
        data['password1'] = 'test1'
        data['password2'] = 'test1'
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password1'][0],
            'This password is too short. It must contain at least 8 characters.')

    def test_validates_user_password_not_entirely_numeric(self):
        data = self.data
        data['password1'] = 45892309
        data['password2'] = 45892309
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password1'][0],
            'This password is entirely numeric.')

    def test_validates_user_password_has_a_special_character(self):
        data = self.data
        data['password1'] = 'AnicePass12'
        data['password2'] = 'AnicePass12'
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password1'][0],
            'Your password should have a special character.')

    def test_validates_user_password_has_a_number(self):
        data = self.data
        data['password1'] = 'AnicePass#'
        data['password2'] = 'AnicePass#'
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password1'][0],
            'Your password should have at least one number.')

    def test_can_send_account_activation_email(self):
        self.assertTrue(self.form.is_valid())
        user = self.form.save()
        self.form.send_account_activation_email(user, self.request)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Welcome to Agripitch 2022!')
        to_email = self.data['email']
        self.assertEqual(mail.outbox[0].to[0], 'agri2022@privateequity-support.com')

    def test_account_activation_email_sent_contains_appropriate_content(self):
        self.form.is_valid()
        user = self.form.save()
        self.form.send_account_activation_email(user, self.request)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('cid:logo.webp', mail.outbox[0].alternatives[0][0])
        self.assertIn('http', mail.outbox[0].alternatives[0][0])
        self.assertIn('testserver', mail.outbox[1].alternatives[0][0])
