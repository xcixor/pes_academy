from django import forms
from common.utils.email import HtmlEmailMixin
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


class InviteSubscriberForm(forms.Form, HtmlEmailMixin):

    email = forms.EmailField()

    def send_invitation_email(self, request):
        to_email = self.cleaned_data['email']
        subject = (
            'Create an account or login to your account to '
            'be able to review applications')
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "email": to_email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject,
            'registration_url': '/accounts/registration/staff/reviewer/'
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='pes_admin/email/reviewer_invitation.html',
            context=context)
