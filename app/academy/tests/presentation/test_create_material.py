from academy.tests.common import AcademyBaseTestCase
from django.urls import reverse, resolve
from academy.presentation.views import UploadMaterialView
from academy.models import SessionMaterial


class UploadMaterialViewTestCase(AcademyBaseTestCase):

    def setUp(self) -> None:
        super(UploadMaterialViewTestCase, self).setUp()
        self.session = self.create_session()

    def test_upload_material(self):
        self.assertEqual(SessionMaterial.objects.count(), 0)
        url = reverse('academy:material_upload', args=[self.session.pk])
        data = {
            'material': self.get_pdf(),
            'material_name': 'Marketing Info',
            'session': self.session
        }
        response = self.client.post(url, data)
        print(response.content)
        self.assertEqual(SessionMaterial.objects.count(), 1)
