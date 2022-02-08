from django.db import models
from django.contrib.auth import get_user_model
from accounts.tests.common import AccountsBaseTestCase


User = get_user_model()


class UserModelTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.user = self.create_user()

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

    def test_can_create_superuser(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'pass1234')
        self.assertEqual(user.email, 'admin@admin.com')

    def test_defines_user_readable_name(self):
        self.assertEqual(str(self.user), 'Jim jones')
