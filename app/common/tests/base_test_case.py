"""Sets up the testing environment."""
import os
import re
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from core.settings.base import BASE_DIR


class BaseTestCase(TestCase):
    """Create the resources required for testing"""

    def delete_test_images(self, path):
        if os.path.isdir(str(BASE_DIR) + path):
            for entry in os.listdir(str(BASE_DIR) + path):
                if re.match('^test_image', entry):
                    os.remove(str(BASE_DIR) + path + entry)

    def get_image(self):
        image_path = str(BASE_DIR) + "/media/tests/test_image.jpg"
        mock_image = SimpleUploadedFile(
            name="test_image.jpg", content=open(image_path, 'rb').read(),
            content_type='image/jpg'
        )
        return mock_image

    def get_pdf(self):
        image_path = str(BASE_DIR) + "/media/tests/test_pdf.pdf"
        mock_image = SimpleUploadedFile(
            name="test_pdf.pdf", content=open(image_path, 'rb').read(),
            content_type='pdf'
        )
        return mock_image

    def create_logged_in_admin(self):
        admin = get_user_model().objects.create_superuser(
            'admin', 'pass1234', email='admin@admin.com')
        self.client.login(username=admin.email, password='pass1234')
        return admin

    def create_normal_user(self):
        user = get_user_model().objects._create_user(
            'normal_user', 'socrates123@')
        user.email = 'socrates@ymail.com'
        user.save()
        return user
