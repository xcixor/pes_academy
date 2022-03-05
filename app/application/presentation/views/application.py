from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from application.models import CallToAction, Application
from application.forms import ApplicationForm
from common.utils.common_queries import get_application


class GetApplicationView(DetailView):

    template_name = "application/application_form.html"
    model = CallToAction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm(self.request)
        user = self.request.user
        application, msg = get_application(user)
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=self.get_object()
            )
        context['application'] = application
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
        business = form.save_business(self.request.user)[0]
        form.save_covid_impact(business)
        form.save_milestone(business)
        form.update_application(self.request.user)
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

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'request': self.request
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs


class ApplicationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationView.as_view()
        return view(request, *args, **kwargs)
