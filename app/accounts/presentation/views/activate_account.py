from django.views.generic import TemplateView


class ActivationEmailSentView(TemplateView):

    template_name = 'registration/activation_email_sent.html'
