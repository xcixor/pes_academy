from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import (
    AdvancedAdminDashboardView, InviteReviewerView, DisplayStaffView,
    MakeStaffReviewerView, ApplicationsView, AssignReviewersView)


class CustomAdmin(admin.AdminSite):

    def get_urls(self):
        return [
            path('',
                 admin.site.admin_view(AdvancedAdminDashboardView.as_view())),
            path('invite/reviewer/',
                 admin.site.admin_view(InviteReviewerView.as_view())),
            path('view/staff/',
                 admin.site.admin_view(DisplayStaffView.as_view())),
            path('make/<int:pk>/reviewer/',
                 admin.site.admin_view(MakeStaffReviewerView.as_view())),
            path('view/applications/',
                 admin.site.admin_view(ApplicationsView.as_view())),
            path('assign/<int:pk>/reviewers/',
                 admin.site.admin_view(AssignReviewersView.as_view())),
        ]


custom_urls = CustomAdmin().get_urls()
