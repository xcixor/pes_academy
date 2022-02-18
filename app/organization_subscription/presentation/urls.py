from django.urls import path
from organization_subscription.presentation.views import (
    InitiateOrganizationSubscriptionView)

app_name = 'organization_subscription'


urlpatterns = [
    path('initiate/',
         InitiateOrganizationSubscriptionView.as_view(), name='help'),
]
