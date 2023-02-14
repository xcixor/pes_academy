from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import (
    AdvancedAdminDashboardView, DisplayStaffView,
    MakeStaffCoachView,
    AllUsersView, RegularUsers, AssignCoachesView)


class CustomAdmin(admin.AdminSite):

    def get_urls(self):
        urls = super(CustomAdmin, self).get_urls()
        custom_urls = [
            path('',
                 admin.site.admin_view(AdvancedAdminDashboardView.as_view()),
                 name='advanced_index'),
            path('view/staff/',
                 admin.site.admin_view(DisplayStaffView.as_view())),
            path('users/all/',
                 admin.site.admin_view(AllUsersView.as_view())),
            path('users/regular/',
                 admin.site.admin_view(RegularUsers.as_view())),
            path('assign/<int:pk>/coaches/',
                 admin.site.admin_view(AssignCoachesView.as_view())),
            path('make/<int:pk>/coach/',
                 admin.site.admin_view(MakeStaffCoachView.as_view())),
        ] + urls
        return custom_urls


custom_pes_admin_site = CustomAdmin(name='admin_advanced')
