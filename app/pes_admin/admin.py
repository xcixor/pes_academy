from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import (
    AdvancedAdminDashboardView, InviteReviewerView, DisplayStaffView,
    MakeStaffReviewerView, ApplicationsView, AssignReviewersView,
    ApplicationDetails, UnassignedApplicationsView,
    InReviewApplicationsView, CreateModerator)


class CustomAdmin(admin.AdminSite):

    def get_urls(self):
        urls = super(CustomAdmin, self).get_urls()
        custom_urls = [
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
            path('applications/unassigned/',
                 admin.site.admin_view(UnassignedApplicationsView.as_view())),
            path('applications/in-review/',
                 admin.site.admin_view(InReviewApplicationsView.as_view())),
            path('assign/<int:pk>/reviewers/',
                 admin.site.admin_view(AssignReviewersView.as_view())),
            path('view/<slug:slug>/',
                 admin.site.admin_view(ApplicationDetails.as_view())),
            path('make/<int:pk>/moderator/',
                 admin.site.admin_view(CreateModerator.as_view())),
        ] + urls
        return custom_urls


custom_pes_admin_site = CustomAdmin(name='Custom PES')
