from django.db import models
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.tests.common import AccountsBaseTestCase


User = get_user_model()


class UserModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(UserModelTestCase, self).setUp()

    def test_email_properties(self):
        field = self.user._meta.get_field('email')
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)
        self.assertIsInstance(field, models.EmailField)

    def test_age_properties(self):
        field = self.user._meta.get_field('age')
        AGE_CHOICES = [
            ('range_one', '20-29'), ('range_two', '30-39'),
            ('range_three', '40-49'), ('range_four', 'Above 50')]
        self.assertIsInstance(field, models.CharField)
        self.assertTrue(field.null)
        self.assertEqual(field.max_length, 20)
        self.assertEqual(field.choices, AGE_CHOICES)

    def test_full_name_properties(self):
        field = self.user._meta.get_field('full_name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_username_properties(self):
        field = self.user._meta.get_field('username')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 40)
        self.assertTrue(field.unique)

    def test_gender_properties(self):
        field = self.user._meta.get_field('gender')
        self.assertEqual(field.max_length, 20)
        self.assertIsInstance(field, models.CharField)
        CHOICES = [('male', 'Male'), ('female', 'Female'),
                   ('undisclosed', 'Prefer not to say'), ('other', 'Other')]
        self.assertEqual(field.choices, CHOICES)

    def test_preferred_language_properties(self):
        field = self.user._meta.get_field('preferred_language')
        self.assertEqual(field.max_length, 40)
        self.assertIsInstance(field, models.CharField)
        CHOICES = [('english', 'English'), ('french', 'French'),
                   ('portuguese', 'Portuguese')]
        self.assertEqual(field.choices, CHOICES)

    def test_has_date_joined_field(self):
        field = self.user._meta.get_field('date_joined')
        self.assertIsInstance(field, models.DateField)
        self.assertTrue(field.auto_now)

    def test_has_is_active(self):
        field = self.user._meta.get_field('is_active')
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)

    def test_can_create_superuser(self):
        user = User.objects.create_superuser('admin', 'pass1234')
        self.assertEqual(user.username, 'admin')

    def test_defines_user_readable_name(self):
        self.assertEqual(str(self.user), str(self.user.id).zfill(3))

    def test_can_get_user_by_uid(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        retrieved_user = User.objects.get_user_by_uid(uid)
        self.assertTrue(retrieved_user)
        self.assertEqual(self.user.email, retrieved_user.email)

    def test_returns_None_if_get_user_by_uid_fails(self):
        uid = 'None'
        self.assertEqual(
            User.objects.get_user_by_uid(uid), None)

    def test_can_create_temporal_user_with_email_only(self):
        user = User.objects.create_temporal_user(email='temp@gmail.com')
        self.assertEqual(user.email, 'temp@gmail.com')
        self.assertTrue(user)
