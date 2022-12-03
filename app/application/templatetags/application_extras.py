from django import template
from django.db.models import Sum
from application.models import ApplicationScore
from agripitch.models import (
    SubCriteriaItem, SubCriteriaItemResponse,
    SubCriteriaItemDocumentResponse)

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
    application_scores = application.scores.exclude(
        reviewer__is_moderator=True)
    total_scores = application_scores.aggregate(Sum('score'))['score__sum']
    reviewers = application.scores.exclude(
        reviewer__is_moderator=True).distinct('reviewer').count()
    average_score = 0
    if total_scores:
        average_score = round(total_scores/reviewers, 2)
    return average_score


@register.filter('get_moderation_score')
def get_moderation_score(application):
    moderation_score = application.scores.filter(
        reviewer__is_moderator=True)
    total_scores = moderation_score.aggregate(Sum('score'))['score__sum']
    reviewers = application.scores.filter(
        reviewer__is_moderator=True).distinct('reviewer').count()
    average_score = 0
    if total_scores:
        average_score = round(total_scores/reviewers, 2)
    return average_score


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


@register.filter('get_applicant_response')
def get_applicant_response(application, sub_criteria_label):
    sub_criteria_item = SubCriteriaItem.objects.get(label=sub_criteria_label)
    response = {}
    if sub_criteria_item.type == 'file':
        saved_response = SubCriteriaItemDocumentResponse.objects.get(
            application=application,
            sub_criteria_item=sub_criteria_item
        )
        response['type'] = 'file'
        response['item'] = saved_response
    elif sub_criteria_item.type == 'countryfield':
        saved_response = SubCriteriaItemResponse.objects.get(
            application=application,
            sub_criteria_item=sub_criteria_item
        )
        response['type'] = 'countryfield'
        response['item'] = saved_response
    else:
        saved_response = SubCriteriaItemResponse.objects.get(
            application=application,
            sub_criteria_item=sub_criteria_item
        )
        response['type'] = 'text'
        response['item'] = saved_response
    return response


@register.filter('get_expected_application_total_score')
def get_expected_application_total_score(multiplier):
    return SubCriteriaItem.objects.count() * int(multiplier)


@register.filter('get_total_questions')
def get_total_questions(string_to_invoke_call):
    return SubCriteriaItem.objects.count()


@register.filter('get_unrated_questions')
def get_unrated_questions(application):
    return SubCriteriaItem.objects.count() - application.marks.count()


@register.filter('get_stage_reviews')
def get_stage_reviews(reviewer, stage):
    total_reviews = reviewer.reviews.all()
    reviews_in_step = total_reviews.filter(application__stage=stage).count()
    return reviews_in_step


@register.filter('get_remaining_reviews')
def get_remaining_reviews(reviewer):
    total_reviews = reviewer.reviews.all()
    reviews_in_step_five = total_reviews.filter(
        application__stage='step_five').count()
    remaining_reviews = total_reviews.count() - reviews_in_step_five
    return remaining_reviews


@register.filter('get_by_qualified_status')
def get_by_qualified_status(reviewer, status):
    total_reviews = reviewer.evaluations.all()
    if status == 'qualified':
        return total_reviews.filter(
            application__disqualified=False,
            application__stage='step_six').count()
    elif status == 'disqualified':
        return total_reviews.filter(
            application__disqualified=True,
            application__stage='step_five').count()
    return 0


@register.filter('get_remaining_evaluations')
def get_remaining_evaluations(reviewer):
    total_reviews = reviewer.reviews.all()
    remaining = total_reviews.filter(
        application__stage='step_five',
        application__disqualified=False).count()
    return remaining
