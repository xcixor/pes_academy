from django.urls import path
from agripitch.presentation.views import (
    ApplicationFormView, AgripitchLandingView, generate_application_pdf)


app_name = 'agripitch'

urlpatterns = [
    path('', AgripitchLandingView.as_view(), name='agripitch_landing_page'),
    path('<slug:slug>/application/',
         ApplicationFormView.as_view(), name='application'),
    path('pdf/', generate_application_pdf, name='generate_application_pdf')
]
