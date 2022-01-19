"""Sets up the testing environment."""
from shutil import rmtree
import os
import re
from django.test import TestCase
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
