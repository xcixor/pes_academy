from django import forms
from django.conf import settings
from application.models import ApplicationPrompt
from common.utils.email import HtmlEmailMixin


class ApplicationPromptForm(forms.ModelForm, HtmlEmailMixin):

    subject = forms.CharField()

    class Meta:
        model = ApplicationPrompt
        fields = ['message', 'application', 'question_position']

    def send_prompt(self, to_email):
        from_email = settings.VERIFIED_EMAIL_USER
        message = self.cleaned_data['message']
        subject = self.cleaned_data['subject']
        context = {
            'message': message
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='application/email/prompt.html', context=context)

    def save(self, reviewer, commit=True):
        prompt = super(ApplicationPromptForm, self).save(commit=False)
        prompt.reviewer = reviewer
        if commit:
            prompt.save()
        return prompt
