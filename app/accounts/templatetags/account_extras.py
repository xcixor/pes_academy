from django import template
from accounts.models import User, Coach


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


@register.filter('get_coach_type')
def get_coach_type(coach, mentee):
    type_of_coach = Coach.objects.get(
        coach=coach, mentee=mentee).get_type_display()
    return type_of_coach
