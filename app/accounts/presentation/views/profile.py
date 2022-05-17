from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ViewProfile(TemplateView, LoginRequiredMixin):

    template_name = 'profile/profile.html'
