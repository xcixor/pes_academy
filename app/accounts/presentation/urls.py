from django.urls import path
from accounts.presentation.views import ApplicationView

urlpatterns = [
    path('applications/<slug:slug>/', ApplicationView.as_view(), name='accounts'),
]
