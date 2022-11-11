from django.urls import path
from eligibility.presentation.views import (
    EligibilityView, ReviewCompleteView, ScoreView, UpdateScoreView,
    DisqualifyView)


app_name = 'eligibility'

urlpatterns = [
    path('<slug:slug>/', EligibilityView.as_view(), name='check_eligibility'),
    path('<slug:slug>/disqualify/', DisqualifyView.as_view(), name='disqualify'),
    path('<slug:slug>/done/', ReviewCompleteView.as_view(),
         name='finish_eligibility'),
    path('<int:pk>/score/', ScoreView.as_view(),
         name='score'),
    path('<int:pk>/score/update/', UpdateScoreView.as_view(),
         name='update_score'),
]
