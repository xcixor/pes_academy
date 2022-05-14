from django.urls import path
from staff.presentation.views import (
    CoacheesView, SessionsView, SessionView, SessionDetails,
    SessionUpdate, SetupMeetingView)


app_name = 'staff'

urlpatterns = [
    path('coachees/', CoacheesView.as_view(), name='coachees'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('session/', SessionView.as_view(), name='session_create'),
    path('session/<int:pk>/', SessionDetails.as_view(), name='session_details'),
    path('session/update/<int:pk>/', SessionUpdate.as_view(), name='session_update'),
    path('meeting/', SetupMeetingView.as_view(), name='meeting_setup'),
]
