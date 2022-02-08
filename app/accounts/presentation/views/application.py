from django.views.generic import DetailView,TemplateView
from sme.models import Application


class ApplicationView(DetailView):

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