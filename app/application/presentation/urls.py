from django.urls import path
from application.presentation.views import (
    IndexView, DraftUserDataView, ApplicationView, SubmitView,
    PostApplicationDocumentFormView, ApplicationPDFView,
    UploadExtraDocuments, ApplicationPrompt, ApplicationScore,
    ApplicationComment)

app_name = 'application'

urlpatterns = [
    path('submit/', SubmitView.as_view(), name='submit'),
    path('prompt/', ApplicationPrompt.as_view(), name='prompt'),
    path('score/', ApplicationScore.as_view(), name='score'),
    path('comment/', ApplicationComment.as_view(), name='comment'),
    path('extra-documents/',
         UploadExtraDocuments.as_view(), name='extra_documents'),
    path('document/', PostApplicationDocumentFormView.as_view(),
         name='document'),
    path('', IndexView.as_view(), name='index'),
    path('<slug:slug>/', ApplicationView.as_view()),
    path('application/draft/', DraftUserDataView.as_view(), name='draft'),
    path('application/pdf/',
         ApplicationPDFView.as_view(), name='application_pdf'),
]
