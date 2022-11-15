from django import template
from accounts.models import User
from organization_subscription.models import Subscription
from eligibility.models import ShortListGroup


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
    application = None
    subscription = Subscription.objects.filter(subscriber_email=email).first()
    if subscription:
        try:
            application = subscription.subscription.subscription_creator.application
        except AttributeError as ae:
            print(ae)
    return application


@register.filter('get_organization_members')
def get_organization_members(email):
    """Fetches members of the same organization as users

    Args:
        email (string): the email to fetch for the user's organization
    usage:
        email|get_organization_members
    Returns:
        list: a list of organization members
    """
    members = []
    try:
        subscription = Subscription.objects.get(subscriber_email=email)
        members_in_db = Subscription.objects.filter(
            subscription=subscription.subscription)
        for member in members_in_db:
            members.append(member)
        members.append(subscription.subscription.subscription_creator.email)
    except Subscription.DoesNotExist as sdne:
        print(sdne)
    return members


@register.filter('is_user_coach')
def is_user_coach(coach, user):
    is_coach = False
    for coaching in user.coaches.all():
        if coaching.coach == coach:
            is_coach = True
    return is_coach


@register.filter('distinct')
def distinct(queryset):
    return queryset.distinct('coach_id')


@register.filter('get_group_slug')
def get_group_slug(step):
    group = ShortListGroup.objects.get(group=step)
    return group.slug
