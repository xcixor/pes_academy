from django.urls import path
from accounts.presentation.views import ApplicationView, DraftUserDataView,SubmitView,HelpView,RegisterView,LoginView

urlpatterns = [
    path('applications/<slug:slug>/', ApplicationView.as_view(), name='accounts'),
    path('application/draft/', DraftUserDataView.as_view(), name='draft'),
    path('submit/', SubmitView.as_view(),name='submit'),
    path('help/', HelpView.as_view(),name='help'),
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
   
]
