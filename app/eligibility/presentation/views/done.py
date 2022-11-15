from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from common.utils.email import HtmlEmailMixin
from application.models import Application
from eligibility.models import ShortListGroup
from agripitch.models import get_sub_criteria_item_response_if_exist
from agripitch.utils import get_sub_criteria_item_by_label


class ReviewCompleteView(SingleObjectMixin, View, HtmlEmailMixin):

    model = Application

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_in_review = False
        self.object.eligibility = True
        self.object.save()
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = settings.ADMIN_EMAILS
        current_site = get_current_site(request)
        context = {
            'user': request.user,
            'application': self.object.special_id,
            'domain': current_site.domain,
            'protocol': request.scheme,
        }
        super().send_email(
            _('Review Completed'), None, from_email, to_email,
            template='eligibility/email/review_done.html',
            context=context)
        return redirect('/accounts/reviewer/applications/')


class StepCompleteView(SingleObjectMixin, View, HtmlEmailMixin):

    model = Application

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        total_marks = sum(mark.score for mark in self.object.marks.all())
        if step.group == 'step_one':
            if total_marks >= 2:
                self.object.stage = 'step_four'
                self.object.eligibility = True
                self.object.save()
            else:
                self.object.disqualified = True
                self.object.save()
        if step.group == 'step_two':
            question_object = get_sub_criteria_item_by_label('Entity Type *')
            application_response = get_sub_criteria_item_response_if_exist(
                question_object, self.object)
            if application_response:
                if application_response.value == 'Start-ups':
                    if total_marks >= 4:
                        self.object.stage = 'step_five'
                        self.object.save()
                    else:
                        self.object.disqualified = True
                        self.object.eligibility = False
                        self.object.save()
                elif application_response.value == 'Mature Startups':
                    if total_marks >= 7:
                        self.object.stage = 'step_five'
                        self.object.save()
                    else:
                        self.object.disqualified = True
                        self.object.eligibility = False
                        self.object.save()
                elif application_response.value == 'Women-Owned':
                    if total_marks >= 7:
                        self.object.stage = 'step_five'
                        self.object.save()
                    else:
                        self.object.disqualified = True
                        self.object.eligibility = False
                        self.object.save()
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = settings.ADMIN_EMAILS
        current_site = get_current_site(request)
        context = {
            'user': request.user,
            'application': self.object.special_id,
            'domain': current_site.domain,
            'protocol': request.scheme,
        }
        super().send_email(
            _('Review Completed'), None, from_email, to_email,
            template='eligibility/email/review_done.html',
            context=context)
        return redirect('/accounts/reviewer/applications/')
