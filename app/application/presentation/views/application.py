from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from application.models import CallToAction, Application
from application.forms import ApplicationForm
from organization_subscription.models import Subscription


class GetApplicationView(DetailView):

    template_name = "application/application_form.html"
    model = CallToAction
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm(self.request)
        user = self.request.user
        application = None
        try:
            application = user.application
        except AttributeError as ae:
            print(ae)
        if not application:
            try:
                subscription = Subscription.objects.get(
                    subscriber_email=user.email)
            except Subscription.DoesNotExist as sd:
                print(sd)
            if subscription:
                application = subscription.subscription.subscription_creator.application
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=self.get_object()
            )
        return context


class PostApplicationView(SingleObjectMixin, FormView):

    template_name = "application/application_form.html"
    form_class = ApplicationForm
    success_url = '/applications/'
    model = CallToAction

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save_application(self.request.user, self.request.object)
        business = form.save_business(self.request.user)[0]
        form.save_covid_impact(business)
        form.save_milestone(business)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = (
            'Great, you application has been received. '
            'We will get back in touch with you.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()

    def form_invalid(self, form):
        success_message = (
            'An error occurred while validating your form. '
            'Please check that all fields are correct. Thank you.')
        messages.add_message(
            self.request, messages.ERROR, success_message)
        return super().form_invalid(form)


class ApplicationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationView.as_view()
        return view(request, *args, **kwargs)
