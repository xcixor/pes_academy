from application.tests.common import ApplicationBaseTestCase
from application.forms import ApplicationDocumentForm
from application.models import ApplicationDocument


class ApplicationDocumentTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(ApplicationDocumentTestCase, self).setUp()
        self.application = self.create_application_instance()
        document = {'document': self.get_pdf()}
        self.form_data = {
            'document_name': 'KRA Pin',
            'application': self.application.pk
        }
        self.form = ApplicationDocumentForm(self.form_data, document)

    def test_form_meta_properties(self):
        self.assertEqual(self.form._meta.model, ApplicationDocument)
        fields = ['document_name', 'document', 'application']
        self.assertEqual([*self.form.fields.keys()], fields)

    def test_this_form_is_valid(self):
        self.assertTrue(self.form.is_valid())
