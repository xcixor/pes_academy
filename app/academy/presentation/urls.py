from django.urls import path
from academy.presentation.views import (
    CoacheesView, SessionsView, SessionView, SessionDetails,
    SessionUpdate, SetupMeetingView, GetSetupMeetingPageView,
    GetMaterialPageView, UploadMaterialView)


app_name = 'academy'

urlpatterns = [
    path('coachees/', CoacheesView.as_view(), name='coachees'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('session/', SessionView.as_view(), name='session_create'),
    path('session/<int:pk>/', SessionDetails.as_view(), name='session_details'),
    path('session/update/<int:pk>/',
         SessionUpdate.as_view(), name='session_update'),
    path('<int:pk>/meeting/', GetSetupMeetingPageView.as_view(), name='meeting_setup'),
    path('<int:pk>/meeting/create/',
         SetupMeetingView.as_view(), name='meeting_create'),
    path('<int:pk>/material/', GetMaterialPageView.as_view(), name='material'),
    path('<int:pk>/material/upload/',
         UploadMaterialView.as_view(), name='material_upload'),
]
