from django.urls import path
from eligibility.presentation.views import (
    EligibilityView, ReviewCompleteView, ScoreView, UpdateScoreView,
    DisqualifyView, EvaluationStepView, StepCompleteView,
    BonusPointsView, DeleteBonusView, RollBackApplicationView,
    ExtraDocumentsView)


app_name = 'eligibility'

urlpatterns = [
    path('<slug:slug>/', EligibilityView.as_view(), name='check_eligibility'),
    path('<slug:slug>/disqualify/', DisqualifyView.as_view(), name='disqualify'),
    path('<slug:slug>/<slug:step_slug>/',
         EvaluationStepView.as_view(), name='step'),
    path('<slug:slug>/<str:step>/<str:current_step>/rollback/',
         RollBackApplicationView.as_view(), name='rollback'),
    path('<slug:slug>/<slug:step_slug>/done',
         StepCompleteView.as_view(), name='step_done'),
    path('<slug:slug>/done/', ReviewCompleteView.as_view(),
         name='finish_eligibility'),
    path('<int:pk>/<slug:application_slug>/<slug:step_slug>/delete/bonus/',
         DeleteBonusView.as_view(), name='delete_bonus'),
    path('<int:pk>/<slug:step_slug>/score/', ScoreView.as_view(),
         name='score'),
    path('<int:pk>/<slug:step_slug>/score/update/', UpdateScoreView.as_view(),
         name='update_score'),
    path('application/<slug:step_slug>/bonus/', BonusPointsView.as_view(),
         name='bonus'),
    path('application/review/docs/<slug:slug>/',
         ExtraDocumentsView.as_view(), name='extra_docs'),
]
