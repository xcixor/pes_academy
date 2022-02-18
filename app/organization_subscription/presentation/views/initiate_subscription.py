from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView
from organization_subscription.forms import InitiateSubscriptionForm

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
        user = User.objects.create_temporal_user(email=email)
        form.send_subscription_email(user, self.request)
        return super().form_valid(form)


class InitiateOrganizationSubscriptionView(View):

    def get(self, request, *args, **kwargs):
        view = GetInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostInitiateOrganizationSubscriptionView.as_view()
        return view(request, *args, **kwargs)
