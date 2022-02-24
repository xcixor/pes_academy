from django.urls import path
from organization_subscription.presentation.views import (
    InitiateOrganizationSubscriptionView, ActivateSubscriptionView)

app_name = 'organization_subscription'


urlpatterns = [
    path('initiate/',
         InitiateOrganizationSubscriptionView.as_view(), name='help'),
    path('activate/',
         ActivateSubscriptionView.as_view(), name='activate'),
]
