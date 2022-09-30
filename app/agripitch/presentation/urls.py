from django.urls import path
from agripitch.presentation.views import (
    ApplicationFormView, AgripitchLandingView,
    generate_application_pdf, DeleteSubCriteriaView,
    GalleryPageView)


app_name = 'agripitch'

urlpatterns = [
    path('', AgripitchLandingView.as_view(), name='agripitch_landing_page'),
    path('<slug:slug>/application/',
         ApplicationFormView.as_view(), name='application'),
    path('pdf/', generate_application_pdf, name='generate_application_pdf'),
    path('subcriteria/responses/delete/',
         DeleteSubCriteriaView.as_view(), name='delete_sub_criteria'),
    path('gallery/',
         GalleryPageView.as_view(), name='gallery')
]
