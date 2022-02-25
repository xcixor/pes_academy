from django import template
from accounts.models import User
from organization_subscription.models import Subscription


register = template.Library()


@register.filter('get_profile')
def get_profile(email):
    """Fetches user profile

    Args:
        email (string): email to filter for user profile

    Returns:
        profile: an object representing the user Profile

    usage:
        email|get_profile
    """
    profile = None
    try:
        profile = User.objects.get(email=email)
    except User.DoesNotExist as udne:
        print(udne)
    return profile


@register.filter('get_application_url')
def get_application_url(email):
    """Returns the users's application url

    Args:
        email (string): user's email

    Returns:
        url: url to for the application
    usage:
        email|get_application_url
    """
    url = None
    subscription = Subscription.objects.filter(subscriber_email=email).first()
    if subscription:
        application = subscription.subscription.subscription_creator.application
        url = f'/applications/{application.call_to_action.slug}/'
    return url
