from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "profile/dashboard.html"

    def get_template_names(self):
        if self.request.user.is_staff:
            return "profile/staff/dashboard.html"
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentors'] = User.objects.filter(is_coach=True)
        return context
