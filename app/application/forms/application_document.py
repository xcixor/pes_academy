from django import forms
from application.models import ApplicationDocument


class ApplicationDocumentForm(forms.ModelForm):

    class Meta:
        model = ApplicationDocument
        fields = '__all__'
