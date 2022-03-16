from django import forms
from application.models import ApplicationScore


class ApplicationScoreForm(forms.Media):

    class Meta:
        model = ApplicationScore
        fields = ['score', 'prompt', 'application']

    def save(self, reviewer, commit=True):
        score = super(ApplicationScoreForm, self).save(commit=False)
        score.reviewer = reviewer
        if commit:
            score.save()
        return score
