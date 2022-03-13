from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ApplicationsToReviewView(LoginRequiredMixin, TemplateView):

    template_name = "profile/staff/applications.html"
