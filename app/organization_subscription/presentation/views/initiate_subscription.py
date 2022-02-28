from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from organization_subscription.forms import InitiateSubscriptionForm
from organization_subscription.models import OrganizationSubscription

User = get_user_model()


class GetInitiateOrganizationSubscriptionView(TemplateView):

    template_name = 'profile/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InitiateSubscriptionForm
        return context


class PostInitiateOrganizationSubscriptionView(FormView):

    template_name = 'profile/dashboard.html'
    success_url = '/accounts/dashboard/'
    form_class = InitiateSubscriptionForm

    def form_valid(self, form):
        email = form.cleaned_data['subscriber_email']
        form.send_subscription_email(email, self.request)
        organization_subscription, created = OrganizationSubscription.objects.update_or_create(
            subscription_creator=self.request.user,
            defaults={
                'subscription_creator': self.request.user
            }
        )
        form.subscribe_user(organization_subscription)
        success_message = (
            f'Great. {email} has been invited to your organization.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = (
            'Hmm..That didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)


class InitiateOrganizationSubscriptionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)
