from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages
from organization_subscription.models import Subscription


class UserLoginView(LoginView):

    template_name = "registration/login.html"

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        success_message = (
            f'Welcome back {self.request.user.username}!')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        user = self.request.user
        application = None
        try:
            application = user.application
        except AttributeError as ae:
            print(ae)
        if not application:
            subscription = None
            try:
                subscription = Subscription.objects.get(
                    subscriber_email=user.email)
            except Subscription.DoesNotExist as sd:
                print(sd)
            if subscription:
                application = subscription.subscription.subscription_creator.application
        if application.status == 'step_one':
            next_url = f'/applications/{application.call_to_action.slug}/'
            return next_url
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return settings.LOGIN_REDIRECT_URL
