from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from common.utils.email import HtmlEmailMixin

User = get_user_model()


class InviteSubscriberForm(forms.Form, HtmlEmailMixin):

    email = forms.EmailField()

    def send_invitation_email(self, request):
        to_email = self.cleaned_data['email']
        # user = None
        try:
            user = User.objects.get(email=to_email)
        except User.DoesNotExist:
            user = None
        url = '/accounts/registration/staff/reviewer/'
        is_registered = False
        if user:
            url = '/accounts/login/'
            is_registered = True
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
            'url': url,
            'is_registered': is_registered
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='pes_admin/email/reviewer_invitation.html',
            context=context)
