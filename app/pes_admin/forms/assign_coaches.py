from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Coach

User = get_user_model()


class AssignCoachesForm(forms.Form):

    coaches = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )
    number_of_coaches = forms.IntegerField(required=False)

    def assign_coaches(self, user):
        coaches = self.cleaned_data['coaches']
        coaches_objects = User.objects.filter(id__in=coaches)
        for coach in coaches_objects:
            Coach.objects.create(
                mentee=user,
                coach=coach
            )
        return True

    def __init__(self, user=None, *args, **kwargs):
        super(AssignCoachesForm, self).__init__(*args, **kwargs)
        if user:
            coach_ids = (coaching.coach.id for coaching in user.coaches.all())
        coaches = User.objects.filter(
            is_coach=True).exclude(id__in=coach_ids)
        COACHES = [
            (coach.id, coach.username)
            for coach in coaches
        ]
        self.fields['coaches'].choices = COACHES
        self.fields['number_of_coaches'].initial = len(COACHES)
