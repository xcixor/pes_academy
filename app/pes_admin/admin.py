from django.urls import path
from django.contrib import admin
from pes_admin.presentation.views import (
    AdvancedAdminDashboardView, InviteReviewerView, DisplayStaffView,
    MakeStaffReviewerView, ApplicationsView, AssignReviewersView,
    ApplicationDetails, UnassignedApplicationsView,
    InReviewApplicationsView, CreateModerator, MakeStaffCoachView,
    AllUsersView, RegularUsers, CallToActionUsers, AssignCoachesView,
    export_inactive_user_emails_to_xls, AdminApplicationView,
    export_remaining_steps_for_users, ClearSortView, ClearSearchView,
    export_emails_without_applications)
from pes_admin.presentation.views.export_form_questions import (
    export_agripitch_questions_xls)
from pes_admin.presentation.views.export_key_stats_to_csv import (
    export_key_stats_to_csv)


class CustomAdmin(admin.AdminSite):

    def get_urls(self):
        urls = super(CustomAdmin, self).get_urls()
        custom_urls = [
            path('',
                 admin.site.admin_view(AdvancedAdminDashboardView.as_view()),
                 name='advanced_index'),
            path('invite/reviewer/',
                 admin.site.admin_view(InviteReviewerView.as_view())),
            path('view/staff/',
                 admin.site.admin_view(DisplayStaffView.as_view())),
            path('make/<int:pk>/reviewer/',
                 admin.site.admin_view(MakeStaffReviewerView.as_view())),
            path(
                'applications/all/',
                admin.site.admin_view(ApplicationsView.as_view()),
                name='all_applications'),
            path('applications/unassigned/',
                 admin.site.admin_view(UnassignedApplicationsView.as_view()),
                 name='unassigned_applications'),
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
            path('application/<slug:slug>/view/',
                 admin.site.admin_view(AdminApplicationView.as_view()),
                 name='admin_application_view'),
            path('view/<slug:slug>/',
                 admin.site.admin_view(ApplicationDetails.as_view())),
            path('make/<int:pk>/moderator/',
                 admin.site.admin_view(CreateModerator.as_view())),
            path('make/<int:pk>/coach/',
                 admin.site.admin_view(MakeStaffCoachView.as_view())),
            path('export/agripitch/xls/', export_agripitch_questions_xls,
                 name='export_agripitch_questions_xls'),
            path(
                'export/users/dormant/xls/',
                export_inactive_user_emails_to_xls,
                name='export_inactive_user_emails_to_xls'),
            path('export/stats/csv/', export_key_stats_to_csv,
                 name='export_key_stats_to_csv'),
            path('export/user/steps/csv/', export_remaining_steps_for_users,
                 name='export_remaining_steps_for_users'),
            path('sort/clear/',
                 admin.site.admin_view(ClearSortView.as_view()),
                 name='clear_sort'),
            path('search/clear/',
                 admin.site.admin_view(ClearSearchView.as_view()),
                 name='clear_search'),
            path('export/user/emails/no/applications/csv/',
                 export_emails_without_applications,
                 name='export_emails_without_applications'),
        ] + urls
        return custom_urls


custom_pes_admin_site = CustomAdmin(name='admin_advanced')
