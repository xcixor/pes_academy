import os
from django import forms
from application.models import ApplicationDocument


class ApplicationDocumentForm(forms.ModelForm):

    class Meta:
        model = ApplicationDocument
        fields = '__all__'

    def save(self, commit=True):
        document, created = ApplicationDocument.objects.update_or_create(
            document_name=self.cleaned_data['document_name'],
            defaults={
                'document': self.cleaned_data['document'],
                'application': self.cleaned_data['application']
            }
        )
        return document

    def clean_document(self):
        document = self.cleaned_data['document']
        extension = os.path.splitext(document.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'Please Upload PDF files only!')
        return document
