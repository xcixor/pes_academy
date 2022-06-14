from django import template
from django.db.models import Avg
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


@register.filter('get_comments')
def get_comments(reviewer, application):
    return reviewer.comments.filter(application=application)


@register.filter('get_question_scores_for_application')
def get_question_scores_for_application(reviewer, application):
    return reviewer.scores.filter(application=application)


@register.filter('get_from_scores')
def get_from_scores(dictionary, key):
    return dictionary.get(key, None)


@register.filter('check_in_queryset')
def check_in_queryset(queryset, key):
    for prompt in queryset:
        if prompt.question_position == key:
            return True
    return False


@register.filter('get_average_score')
def get_average_score(application):
    average_score = application.scores.exclude(
        reviewer__is_moderator=True).aggregate(Avg('score'))
    return average_score['score__avg']


@register.filter('get_moderation_score')
def get_moderation_score(application):
    moderation_score = application.scores.exclude(
        reviewer__is_reviewer=True).aggregate(Avg('score'))
    return moderation_score['score__avg']


@register.filter('in_progress')
def in_progress(application_reviews):
    if application_reviews:
        return application_reviews.filter(application__stage='step_three')


@register.filter('review_finished')
def review_finished(application_reviews):
    if application_reviews:
        return application_reviews.filter(application__stage='step_four')


@register.filter('get_document')
def get_document(application, document_name):
    if application:
        document = application.documents.filter(
            document_name=document_name).first()
        return document
    return None
