from django.urls import path
from home.presentation.views import (
    IndexView, PrivacyPolicyView)

app_name = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
]
