from django.contrib import admin
from django.urls import path
from pes_admin.presentation.views import (AdvancedAdminDashboardView)


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super(CustomAdminSite, self).get_urls()
        custom_urls = [
            path('advanced/',
                 self.admin_view(AdvancedAdminDashboardView.as_view()),
                 name="dashboard"),
        ] + urls
        return custom_urls


custom_admin_site = CustomAdminSite(name='PES Admin')
