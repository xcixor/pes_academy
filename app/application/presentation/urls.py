from django.urls import path
from application.presentation.views import (
    IndexView, SubmitView,
    PostApplicationDocumentFormView, ApplicationPDFView,
    UploadExtraDocumentsView, ApplicationPromptView, ApplicationScoreView,
    ApplicationCommentView, PrivacyPolicyView)

app_name = 'application'

urlpatterns = [
    path('applications/submit/', SubmitView.as_view(), name='submit'),
    path('applications/prompt/', ApplicationPromptView.as_view(), name='prompt'),
    path('applications/score/<slug:slug>/',
         ApplicationScoreView.as_view(), name='score'),
    path('applications/comment/', ApplicationCommentView.as_view(), name='comment'),
    path('applications/extra-documents/',
         UploadExtraDocumentsView.as_view(), name='extra_documents'),
    path('applications/document/', PostApplicationDocumentFormView.as_view(),
         name='document'),
    path('', IndexView.as_view(), name='index'),
    path('applications/application/pdf/',
         ApplicationPDFView.as_view(), name='application_pdf'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
]
