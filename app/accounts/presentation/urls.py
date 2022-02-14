from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.presentation.views import (
    HelpView, UserLoginView, RegistrationView, ActivationEmailSentView,
    AccountActivationView)

app_name = 'accounts'

urlpatterns = [
    path('help/', HelpView.as_view(),name='help'),
    path('register/', RegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='/applications/')),
    path('activation-email-sent/', ActivationEmailSentView.as_view(),
          name='activation_email_sent'),
    path('activate/<str:uidb64>/<str:token>/',
         AccountActivationView.as_view(), name='activate'),
]
