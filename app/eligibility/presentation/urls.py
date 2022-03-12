from django.urls import path
from eligibility.presentation.views import EligibilityView


app_name = 'eligibility'

urlpatterns = [
    path('<slug:slug>/', EligibilityView.as_view(), name='check_eligibility')
]
