from django import template
from application.models import ApplicationScore

register = template.Library()


@register.filter('get_reviewer_scores_for_application')
def get_reviewer_scores_for_application(reviewer, application):
    scores = ApplicationScore.objects.filter(
        reviewer=reviewer,
        application=application
    )
    return sum(item.score for item in scores)


@register.filter('get_prompts')
def get_prompts(reviewer, application):
    return reviewer.prompts.filter(application=application)
