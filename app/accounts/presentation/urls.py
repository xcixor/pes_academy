from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.presentation.views import (
    HelpView, UserLoginView, RegistrationView)

app_name = 'accounts'

urlpatterns = [
    path('help/', HelpView.as_view(),name='help'),
    path('register/', RegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='/applications/')),
]
