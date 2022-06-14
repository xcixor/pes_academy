from django.urls import path
from application.presentation.views import (
    IndexView, DraftApplicationDataView, ApplicationView, SubmitView,
    PostApplicationDocumentFormView, ApplicationPDFView,
    UploadExtraDocumentsView, ApplicationPromptView, ApplicationScoreView,
    ApplicationCommentView, DraftUserInfoView)

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
    path('applications/<slug:slug>/', ApplicationView.as_view()),
    path('applications/application/draft/',
         DraftApplicationDataView.as_view(), name='draft'),
    path('applications/user/info/',
         DraftUserInfoView.as_view(), name='draft_user'),
    path('applications/application/pdf/',
         ApplicationPDFView.as_view(), name='application_pdf'),
]
