from academy.tests.common import AcademyBaseTestCase
from django.urls import reverse, resolve
from academy.presentation.views import GetMaterialPageView


class GetMaterialPageTestCase(AcademyBaseTestCase):

    def setUp(self) -> None:
        super(GetMaterialPageTestCase, self).setUp()
        self.session = self.create_session()

    def test_successfully_gets_material_page(self):
        url = reverse('academy:material', args=[self.session.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/material.html')

    def test_get_create_meeting_url_resolves(self):
        url = reverse('academy:material', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, GetMaterialPageView)
