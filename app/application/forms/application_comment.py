from django import forms
from application.models import ApplicationComment


class ApplicationCommentForm(forms.ModelForm):

    class Meta:
        model = ApplicationComment
        fields = ['comment', 'application']

    def save(self, reviewer, commit=True):
        prompt = super(ApplicationCommentForm, self).save(commit=False)
        prompt.reviewer = reviewer
        if commit:
            prompt.save()
        return prompt
