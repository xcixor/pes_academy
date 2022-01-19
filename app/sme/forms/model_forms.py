from django import forms
from sme.models import Application


class ApplicationAdminForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ApplicationAdminForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = forms.HiddenInput()
        self.fields['slug'].widget.attrs['readonly'] = True
