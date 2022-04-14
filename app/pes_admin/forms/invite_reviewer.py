from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from common.utils.email import HtmlEmailMixin


class InviteSubscriberForm(forms.Form, HtmlEmailMixin):

    email = forms.EmailField()

    def send_invitation_email(self, request):
        to_email = self.cleaned_data['email']
        subject = _(
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
