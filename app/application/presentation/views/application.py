from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import SingleObjectMixin
from application.models import CallToAction, Application
from application.forms import ApplicationForm
from common.utils.common_queries import get_application


class GetApplicationFormView(TemplateView):

    template_name = "application/application_form.html"

    def get_context_data(self, **kwargs):
        call_to_action_slug = kwargs.get('slug')
        call_to_action = CallToAction.objects.get(slug=call_to_action_slug)
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm(self.request)
        user = self.request.user
        application, msg = get_application(user)
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=call_to_action
            )
        context['application'] = application
        return context


class PostApplicationView(SingleObjectMixin, FormView):

    template_name = "application/application_form.html"
    form_class = ApplicationForm
    success_url = '/'
    model = CallToAction

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        business = form.save_business(self.request.user)[0]
        form.save_covid_impact(business)
        form.update_application(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _(
            'Great, you application has been received. '
            'We will get back in touch with you.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()

    def form_invalid(self, form):
        error_message = _(
            'An error occurred while validating your form. '
            'Please check that all fields are correct. Thank you.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
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
        view = GetApplicationFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationView.as_view()
        return view(request, *args, **kwargs)
