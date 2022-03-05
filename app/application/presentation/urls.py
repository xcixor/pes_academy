from django.urls import path
from application.presentation.views import (
    IndexView, DraftUserDataView, ApplicationView, SubmitView,
    PostApplicationDocumentFormView)

app_name = 'application'

urlpatterns = [
    path('submit/', SubmitView.as_view(), name='submit'),
    path('document/', PostApplicationDocumentFormView.as_view(),
         name='document'),
    path('', IndexView.as_view(), name='index'),
    path('<slug:slug>/', ApplicationView.as_view()),
    path('application/draft/', DraftUserDataView.as_view(), name='draft'),
]
