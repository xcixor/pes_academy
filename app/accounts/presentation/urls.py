from django.urls import path
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView)
from accounts.presentation.views import (
    HelpView, UserLoginView, RegistrationView, ActivationEmailSentView,
    AccountActivationView, DashboardView, ReviewerRegistrationView,
    ApplicationsToReviewView, CoachBio, Coaching, CoachSessions, SessionView,
    ViewProfile, EditProfile, PasswordChangeView, PasswordResetView,
    ResendActivationEmailView)

app_name = 'accounts'

urlpatterns = [
    path('help/', HelpView.as_view(), name='help'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/resend_activation_email/',
         ResendActivationEmailView.as_view(), name='resend_activation_email'),
    path('register/staff/reviewer/', ReviewerRegistrationView.as_view(),
         name='reviewer_registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('activation-email-sent/', ActivationEmailSentView.as_view(),
         name='activation_email_sent'),
    path('activate/<str:uidb64>/<str:token>/',
         AccountActivationView.as_view(), name='activate'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ViewProfile.as_view(), name='profile_view'),
    path('profile/edit/<int:pk>/', EditProfile.as_view(), name='profile_edit'),
    path(
        'password/change/',
        PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', PasswordResetView.as_view(),
         name='password_reset_request'),
    path('password/reset/', PasswordResetCompleteView.as_view(
        template_name='registration/password/password_reset_complete.html'),
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="registration/password/password_reset_confirm.html",
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password/password_reset_complete.html'),
        name='password_reset_complete'),
    path('reviewer/applications/',
         ApplicationsToReviewView.as_view(), name='applications_to_review'),
    path('bio/<int:pk>/', CoachBio.as_view(), name='mentor_bio'),
    path('mentor/add/', Coaching.as_view(), name='coaching'),
    path('mentor/sessions/<int:pk>/', CoachSessions.as_view(), name='sessions'),
    path('session/<int:pk>/', SessionView.as_view(), name='session'),
]
