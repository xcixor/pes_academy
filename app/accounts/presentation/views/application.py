from django.contrib.auth.views import LoginView
from django.conf import settings
from django.views.generic import DetailView,TemplateView
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from sme.models import Application
from accounts.forms import ApplicationForm


class GetApplicationView(DetailView):

    template_name = "application_form.html"
    model = Application
    context_object_name = 'application'


class SubmitView(TemplateView):
    template_name = "submit.html"

class HelpView(TemplateView):
    template_name = "help.html"


class UserLoginView(LoginView):

    template_name = "login.html"

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        success_message = (
            f'Welcome back {self.request.user.username}!')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        next_url = self.request.GET.get("next", None)
        if next_url is None:
            return settings.LOGIN_REDIRECT_URL
        return next_url


class PostApplicationView(SingleObjectMixin, FormView):

    template_name = "application_form.html"
    form_class = ApplicationForm
    success_url = '/'
    model = Application

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save_user()[0]
        business = form.save_business(user)[0]
        business.application = self.object
        business.save()
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


class ApplicationView(View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationView.as_view()
        return view(request, *args, **kwargs)
