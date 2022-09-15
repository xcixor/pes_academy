from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import (
    AdvancedAdminDashboardView, InviteReviewerView, DisplayStaffView,
    MakeStaffReviewerView, ApplicationsView, AssignReviewersView,
    ApplicationDetails, UnassignedApplicationsView,
    InReviewApplicationsView, CreateModerator, MakeStaffCoachView,
    AllUsersView, RegularUsers, CallToActionUsers, AssignCoachesView,
    SubCriteriaItemFieldPropertiesView)
from pes_admin.presentation.views.export_form_questions import export_agripitch_questions_xls


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
            path('users/all/',
                 admin.site.admin_view(AllUsersView.as_view())),
            path('users/regular/',
                 admin.site.admin_view(RegularUsers.as_view())),
            path('users/call-to-action/',
                 admin.site.admin_view(CallToActionUsers.as_view())),
            path('assign/<int:pk>/coaches/',
                 admin.site.admin_view(AssignCoachesView.as_view())),
            path('assign/<int:pk>/reviewers/',
                 admin.site.admin_view(AssignReviewersView.as_view())),
            path('view/<slug:slug>/',
                 admin.site.admin_view(ApplicationDetails.as_view())),
            path('make/<int:pk>/moderator/',
                 admin.site.admin_view(CreateModerator.as_view())),
            path('make/<int:pk>/coach/',
                 admin.site.admin_view(MakeStaffCoachView.as_view())),
            path('export/agripitch/xls/', export_agripitch_questions_xls,
                 name='export_agripitch_questions_xls'),
            path('create/subcriteria/property/',
                 SubCriteriaItemFieldPropertiesView.as_view()),
        ] + urls
        return custom_urls


custom_pes_admin_site = CustomAdmin(name='Custom PES')
