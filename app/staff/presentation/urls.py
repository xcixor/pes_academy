from django.urls import path
from staff.presentation.views import CoacheesView


app_name = 'staff'

urlpatterns = [
    path('coachees/', CoacheesView.as_view(), name='coachees'),
]
