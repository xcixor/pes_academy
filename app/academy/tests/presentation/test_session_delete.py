from django.urls import reverse, resolve
from academy.tests.common import AcademyBaseTestCase
from academy.presentation.views import DeleteSessionView
from academy.models import Session


class DeleteSessionViewTestCase(AcademyBaseTestCase):

    def setUp(self):
        super(DeleteSessionViewTestCase, self).setUp()
        self.session = self.create_session()

    def test_url_resolves(self):
        url = reverse('academy:delete_session', args=[self.session.pk])
        self.assertEqual(resolve(url).func.view_class, DeleteSessionView)

    def test_delete_session(self):
        self.assertTrue(Session.objects.get(
            pk=self.session.pk))
        url = reverse('academy:delete_session', args=[self.session.pk])
        self.client.post(url)
        with self.assertRaises(Session.DoesNotExist):
            Session.objects.get(pk=self.session.pk)
        with self.assertRaisesMessage(
                Session.DoesNotExist,
                'Session matching query does not exist.'):
            Session.objects.get(pk=self.session.pk)
