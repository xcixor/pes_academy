from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login
from accounts.forms import RegistrationForm


class GetRegistrationView(TemplateView):

    template_name = 'registration/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm
        return context


class PostRegistrationView(FormView):

    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accounts/login/'


    def form_valid(self, form):
        self.request.session.pop('registration_details', None)
        authenticated_user = form.save()
        login(self.request, authenticated_user)
        return super().form_valid(form)

    def form_invalid(self, form):
        registration_details = {}
        for key, value in self.request.POST.items():
            registration_details[key] = value
        registration_details.pop('password1')
        registration_details.pop('password2')
        self.request.session['registration_details'] = registration_details
        return super().form_invalid(form)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        view = GetRegistrationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostRegistrationView.as_view()
        return view(request, *args, **kwargs)