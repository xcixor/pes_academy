from django.views.generic import DetailView,TemplateView
from django.views import View
from django.views.generic import DetailView, FormView
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

class RegisterView(TemplateView):
    template_name = "register.html"

class LoginView(TemplateView):
    template_name = "login.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm
        return context


class PostApplicationView(FormView):

    template_name = "application_form.html"
    form_class = ApplicationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save_user()[0]
        business = form.save_business(user)[0]
        form.save_covid_impact(business)
        form.save_milestone(business)
        return super().form_valid(form)

class ApplicationView(View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationView.as_view()
        return view(request, *args, **kwargs)
