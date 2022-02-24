from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView
from organization_subscription.forms import InitiateSubscriptionForm
from organization_subscription.models import OrganizationSubscription

User = get_user_model()


class GetInitiateOrganizationSubscriptionView(TemplateView):

    template_name = 'organization_subscription/initiate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InitiateSubscriptionForm
        return context


class PostInitiateOrganizationSubscriptionView(FormView):

    template_name = 'organization_subscription/initiate.html'
    success_url = '/organization-subscription/initiate/'
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
        return super().form_valid(form)


class InitiateOrganizationSubscriptionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)
