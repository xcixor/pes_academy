from django.urls import path
from staff.presentation.views import (
    CoacheesView, SessionsView, SessionView)


app_name = 'staff'

urlpatterns = [
    path('coachees/', CoacheesView.as_view(), name='coachees'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('session/', SessionView.as_view(), name='session_create'),
]
