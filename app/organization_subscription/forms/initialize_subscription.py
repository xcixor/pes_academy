from django import forms
from common.utils.email import HtmlEmailMixin
from accounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from organization_subscription.models import Subscription


class InitiateSubscriptionForm(forms.Form, HtmlEmailMixin):

    subscriber_email = forms.EmailField()

    def subscribe_user(self, organization_subscription):
        email = self.cleaned_data['subscriber_email']
        try:
            subscription = Subscription.objects.get(subscriber_email=email)
            if subscription:
                raise forms.ValidationError(
                    'This user is already subscribed to your organization')
        except Subscription.DoesNotExist:
            subscription = Subscription.objects.create(
                subscriber_email=email, subscription=organization_subscription)
        return subscription

    def send_subscription_email(self, user, request):
        to_email = user.email
        subject = "Join Our Organization Channel"
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "email": user.email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='organization_subscription/email/organization_subscription.html',
            context=context)
