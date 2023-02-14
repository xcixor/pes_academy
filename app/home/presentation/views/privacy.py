from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):

    template_name = 'privacy/privacy.html'
