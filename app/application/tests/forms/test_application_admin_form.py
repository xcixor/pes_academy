from django import forms
from application.tests.common import ApplicationBaseTestCase
from application.forms import ApplicationAdminForm


class ApplicationAdminFormTestCase(ApplicationBaseTestCase):

    def setUp(self):
        self.data = {
            'image': self.get_image(),
            'tagline': 'Call For Application 1',
            'description': 'Applications for agribusiness',
            'slug': 'call-for-application-1',
            'deadline': '2022-01-10 14:38:50.813404+00:00'
        }
        self.form = ApplicationAdminForm(self.data)

    def test_defines_fields(self):
        fields = [
            'image', 'tagline', 'description', 'slug',
            'deadline', 'available_for_applications']
        self.assertEqual([*self.form.fields.keys()], fields)

    def test_slug_field_extra_properties(self):
        self.assertTrue(self.form.fields['slug'].widget.attrs['readonly'])
        self.assertTrue(isinstance(
            self.form.fields['slug'].widget, forms.HiddenInput))
