from django import forms
from django.contrib.auth import get_user_model
from application.models import ApplicationReview

User = get_user_model()


class AssignReviewersForm(forms.Form):

    reviewers = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )

    def assign_reviewers(self, application):
        reviewers = self.cleaned_data['reviewers']
        reviewer_objects = User.objects.filter(id__in=reviewers)
        for reviewer in reviewer_objects:
            ApplicationReview.objects.create(
                application=application,
                reviewer=reviewer
            )
        return True

    def __init__(self, *args, **kwargs):
        super(AssignReviewersForm, self).__init__(*args, **kwargs)
        reviewers = User.objects.filter(is_staff=True, is_superuser=False)
        REVIEWERS = [
            (reviewer.id, reviewer.username)
            for reviewer in reviewers
        ]
        self.fields['reviewers'].choices = REVIEWERS
