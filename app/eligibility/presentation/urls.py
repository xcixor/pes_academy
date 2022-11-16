from django.urls import path
from eligibility.presentation.views import (
    EligibilityView, ReviewCompleteView, ScoreView, UpdateScoreView,
    DisqualifyView, EvaluationStepView, StepCompleteView,
    BonusPointsView)


app_name = 'eligibility'

urlpatterns = [
    path('<slug:slug>/', EligibilityView.as_view(), name='check_eligibility'),
    path('<slug:slug>/<slug:step_slug>/',
         EvaluationStepView.as_view(), name='step'),
    path('<slug:slug>/<slug:step_slug>/done',
         StepCompleteView.as_view(), name='step_done'),
    path('<slug:slug>/disqualify/', DisqualifyView.as_view(), name='disqualify'),
    path('<slug:slug>/done/', ReviewCompleteView.as_view(),
         name='finish_eligibility'),
    path('<int:pk>/<slug:step_slug>/score/', ScoreView.as_view(),
         name='score'),
    path('<int:pk>/<slug:step_slug>/score/update/', UpdateScoreView.as_view(),
         name='update_score'),
    path('application/<slug:step_slug>/bonus/', BonusPointsView.as_view(),
         name='bonus'),
]
