from django.urls import path
from accounts.presentation.views import ApplicationView

urlpatterns = [
    path('', ApplicationView.as_view()),
]