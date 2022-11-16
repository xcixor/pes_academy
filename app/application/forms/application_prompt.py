from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from application.models import ApplicationPrompt
from common.utils.email import HtmlEmailMixin


class ApplicationPromptForm(forms.ModelForm, HtmlEmailMixin):

    subject = forms.CharField()

    class Meta:
        model = ApplicationPrompt
        fields = ['message', 'application', 'prompt']

    def send_prompt(self, to_email, reply_to, request):
        from_email = settings.VERIFIED_EMAIL_USER
        message = self.cleaned_data['message']
        subject = self.cleaned_data['subject']
        current_site = get_current_site(request)
        context = {
            'message': message,
            'domain': current_site.domain,
            'protocol': request.scheme,
        }
        headers = {'Reply-To': reply_to}
        super().send_email(
            subject, None, from_email, [to_email], headers=headers,
            template='application/email/prompt.html', context=context)

    def save(self, reviewer, commit=True):
        prompt = super(ApplicationPromptForm, self).save(commit=False)
        prompt.reviewer = reviewer
        if commit:
            prompt.save()
        return prompt
