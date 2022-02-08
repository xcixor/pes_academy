from django.test import TestCase
from django import forms
from accounts.forms import RegistrationForm
from accounts.models import User


class RegistrationFormTestCase(TestCase):

    def setUp(self):
        self.data = {
            'email': 'testuser@gmail.com',
            'password1': 'cli3ntnu1#',
            'password2': 'cli3ntnu1#',
            'username': 'pish_dush'
        }
        self.form = RegistrationForm(self.data)

    def test_specifies_model(self):
        self.assertIsInstance(self.form.Meta.model(), User)

    def test_defines_fields(self):
        self.assertTrue(self.form.fields['email'])
        self.assertTrue(self.form.fields['password1'])
        self.assertTrue(self.form.fields['password2'])

    def test_password_1_properties(self):
        self.assertIsInstance(
            self.form.fields['password1'].widget, forms.PasswordInput)
        self.assertEqual(self.form.fields['password1'].label, 'Password')

    def test_password_2_properties(self):
        self.assertIsInstance(
            self.form.fields['password2'].widget, forms.PasswordInput)
        self.assertEqual(
            self.form.fields['password2'].label, 'Confirm Password')

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
        self.form.save()
        saved_user = User.objects.get(email=self.data['email'])
        self.assertEqual(saved_user.username, self.data['username'])

    def test_can_save_transcriber_user(self):
        self.data['is_transcriber'] = True
        form = RegistrationForm(self.data)
        form.save()
        saved_user = User.objects.get(email=self.data['email'])
        self.assertEqual(saved_user.username, self.data['username'])

    def test_saves_user_with_password(self):
        self.form.save()
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