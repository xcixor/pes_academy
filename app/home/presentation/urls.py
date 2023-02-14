from django.urls import path
from application.presentation.views import (
    IndexView, PrivacyPolicyView)

app_name = 'application'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
]
