from django.urls import path
from application.presentation.views import (
    IndexView, SubmitView,
    PostApplicationDocumentFormView, UploadExtraDocumentsView,
    ApplicationPromptView, ApplicationScoreView,
    ApplicationCommentView, PrivacyPolicyView, StepApplicationCommentView)

app_name = 'application'

urlpatterns = [
    path('applications/submit/', SubmitView.as_view(), name='submit'),
    path('applications/prompt/', ApplicationPromptView.as_view(), name='prompt'),
    path('applications/score/<slug:slug>/',
         ApplicationScoreView.as_view(), name='score'),
    path('eligibility/comment/<slug:slug>/<slug:step_slug>/',
         StepApplicationCommentView.as_view(), name='step_comment'),
    path('applications/comment/', ApplicationCommentView.as_view(), name='comment'),
    path('applications/extra-documents/',
         UploadExtraDocumentsView.as_view(), name='extra_documents'),
    path('applications/document/', PostApplicationDocumentFormView.as_view(),
         name='document'),
    path('', IndexView.as_view(), name='index'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
]
