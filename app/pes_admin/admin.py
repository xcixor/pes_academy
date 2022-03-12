from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import AdvancedAdminDashboardView


class CustomAdmin(admin.AdminSite):

    def get_urls(self):
        return [
            path('',
                 admin.site.admin_view(AdvancedAdminDashboardView.as_view())),
        ]


custom_urls = CustomAdmin().get_urls()
