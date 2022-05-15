from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.presentation.views import (
    HelpView, UserLoginView, RegistrationView, ActivationEmailSentView,
    AccountActivationView, DashboardView, ReviewerRegistrationView,
    ApplicationsToReviewView, CoachBio, Coaching, CoachSessions)

app_name = 'accounts'

urlpatterns = [
    path('help/', HelpView.as_view(), name='help'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/staff/reviewer/', ReviewerRegistrationView.as_view(),
         name='reviewer_registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('activation-email-sent/', ActivationEmailSentView.as_view(),
         name='activation_email_sent'),
    path('activate/<str:uidb64>/<str:token>/',
         AccountActivationView.as_view(), name='activate'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reviewer/applications/',
         ApplicationsToReviewView.as_view(), name='applications_to_review'),
    path('bio/<int:pk>/', CoachBio.as_view(), name='mentor_bio'),
    path('mentor/add/', Coaching.as_view(), name='coaching'),
    path('mentor/sessions/<int:pk>/', CoachSessions.as_view(), name='sessions'),
]
