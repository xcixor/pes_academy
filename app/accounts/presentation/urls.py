from django.urls import path
from accounts.presentation.views import ApplicationView, DraftUserDataView

urlpatterns = [
    path('applications/<slug:slug>/', ApplicationView.as_view(), name='accounts'),
    path('application/draft/', DraftUserDataView.as_view(), name='draft'),
]
