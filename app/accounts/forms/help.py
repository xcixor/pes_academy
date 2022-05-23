from django import forms
from django.utils import timezone
from django.conf import settings
from common.utils.email import HtmlEmailMixin


class HelpForm(forms.Form, HtmlEmailMixin):

    name = forms.CharField(max_length=200, required=True)
    subject = forms.CharField(max_length=400, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(), required=True)

    def send_email(self, *args, **kwargs):
        subject = self.cleaned_data['subject']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = settings.SUPPORT_EMAILS
        context = {
            'email_address': email,
            'name': name,
            'subject': subject,
            'message': message,
            'date': timezone.now()
        }
        return super().send_email(
            subject, None, from_email, to_email,
            template='email/help/help_email.html',
            context=context)
