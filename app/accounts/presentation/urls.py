from django.urls import path
from accounts.presentation.views import (
    HelpView, UserLoginView, RegistrationView)

app_name = 'accounts'

urlpatterns = [
    path('help/', HelpView.as_view(),name='help'),
    path('register/', RegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
]
