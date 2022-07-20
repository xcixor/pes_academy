from django.urls import path
from agripitch.presentation.views import ApplicationFormView


app_name = 'agripitch'

urlpatterns = [
    path('<slug:slug>/application/',
         ApplicationFormView.as_view(), name='application')
]
