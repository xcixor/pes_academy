from django import forms
from common.utils.email import HtmlEmailMixin
from django.contrib.sites.shortcuts import get_current_site
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

    def send_subscription_email(self, to_email, request):
        print('sending')
        subject = "Join Our Organization Channel"
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "email": to_email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='organization_subscription/email/organization_subscription.html',
            context=context)
