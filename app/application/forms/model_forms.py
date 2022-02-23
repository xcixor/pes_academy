from django import forms
from application.models import CallToAction


class CallToActionAdminForm(forms.ModelForm):

    class Meta:
        model = CallToAction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CallToActionAdminForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = forms.HiddenInput()
        self.fields['slug'].widget.attrs['readonly'] = True
