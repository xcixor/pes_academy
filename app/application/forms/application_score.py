from django import forms
from application.models import ApplicationScore


class ApplicationScoreForm(forms.ModelForm):

    class Meta:
        model = ApplicationScore
        fields = ['score', 'prompt', 'application']

    def save(self, reviewer):
        score, created = ApplicationScore.objects.update_or_create(
            prompt=self.cleaned_data['prompt'],
            reviewer=reviewer,
            defaults={
                'score': self.cleaned_data['score'],
                'application': self.cleaned_data['application'],
            }
        )
        return score
