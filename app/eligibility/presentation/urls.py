from django.urls import path
from eligibility.presentation.views import (
    EligibilityView, ReviewCompleteView)


app_name = 'eligibility'

urlpatterns = [
    path('<slug:slug>/', EligibilityView.as_view(), name='check_eligibility'),
    path('<slug:slug>/done/', ReviewCompleteView.as_view(),
         name='finish_eligibility'),
]
