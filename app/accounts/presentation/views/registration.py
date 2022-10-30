from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login
from django_htmx.http import HttpResponseClientRedirect
from accounts.forms import RegistrationForm


class GetRegistrationView(TemplateView):

    template_name = 'registration/registration.html'

    def get_template_names(self):
        request_origin = self.request.resolver_match.view_name
        if request_origin == 'accounts:reviewer_registration':
            return 'registration/staff_registration.html'
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm
        return context


class PostRegistrationView(FormView):

    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    partial_template_name = 'registration/partial/registration.html'
    success_url = '/'

    def form_valid(self, form):
        self.partial_template_name = 'registration/partial/registration_success.html'
        self.request.session.pop('registration_details', None)
        new_user = form.save()
        if not settings.DEBUG:
            form.send_account_activation_email(new_user, self.request)
        login(self.request, new_user)
        success_message = _("Registration successful, start your application!")
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        if self.request.htmx:
            return HttpResponseClientRedirect(self.success_url)
        return super().form_valid(form)

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name

    def form_invalid(self, form):
        registration_details = {}
        for key, value in self.request.POST.items():
            registration_details[key] = value
        registration_details.pop('password1', None)
        registration_details.pop('password2', None)
        self.request.session['registration_details'] = registration_details
        return super().form_invalid(form)


class PostReviewerRegistrationView(FormView):

    form_class = RegistrationForm
    template_name = 'registration/staff_registration.html'
    success_url = '/accounts/dashboard/'

    def form_valid(self, form):
        self.request.session.pop('registration_details', None)
        inactive_user = form.save()
        inactive_user.is_active = True
        inactive_user.is_staff = True
        inactive_user.save()
        success_message = _("Registration successful!")
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        login(self.request, inactive_user)
        return super().form_valid(form)

    def form_invalid(self, form):
        registration_details = {}
        for key, value in self.request.POST.items():
            registration_details[key] = value
        registration_details.pop('password1', None)
        registration_details.pop('password2', None)
        self.request.session['registration_details'] = registration_details
        error_message = _("Please correct the errors in your form")
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        view = GetRegistrationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostRegistrationView.as_view()
        return view(request, *args, **kwargs)


class ReviewerRegistrationView(View):

    def get(self, request, *args, **kwargs):
        view = GetRegistrationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostReviewerRegistrationView.as_view()
        return view(request, *args, **kwargs)
