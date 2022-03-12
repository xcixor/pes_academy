from django.views.generic import TemplateView


class AdvancedAdminDashboardView(TemplateView):

    template_name = 'pes_admin/dashboard.html'
