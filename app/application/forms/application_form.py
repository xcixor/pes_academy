from django import forms
from application.models import BusinessOrganization, Milestone, CovidImpact
from accounts.models import User

class ApplicationForm(forms.Form):

    full_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'text draftable'}))
    age = forms.ChoiceField(
        choices=User.AGE_CHOICES, widget=forms.RadioSelect)
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.RadioSelect)
    preferred_language = forms.ChoiceField(
        widget=forms.RadioSelect, choices=User.LANGUAGE_CHOICES)
    organization_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'text draftable'}))
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable'}))
    twitter_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable'}))
    instagram_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable'}))
    linkedin_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable'}))
    whatsapp_business_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable'}))
    value_chain = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=BusinessOrganization.VALUE_CHAIN_CHOICES)
    existence_period = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=BusinessOrganization.EXISTENCE_PERIOD_CHOICES)
    stage = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=BusinessOrganization.STAGE_CHOICES)
    impact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'text draftable'}))
    milestones = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_milestones(self):
        milestones = self.cleaned_data['milestones']
        if len(milestones) > 3:
            raise forms.ValidationError('You cannot select more than 3 items.')
        return milestones

    def save_user(self, email):
        if self.is_valid():
            user, created = User.objects.update_or_create(
                email=email,
                defaults={
                    'full_name': self.cleaned_data['full_name'],
                    'age': self.cleaned_data['age'],
                    'gender': self.cleaned_data['gender'],
                    'preferred_language': self.cleaned_data['preferred_language']
                }

            )
            return user, created
        return None

    def save_business(self, user):
        if self.is_valid():
            business, created = BusinessOrganization.objects.update_or_create(
                organization_owner=user,
                organization_name=self.cleaned_data['organization_name'],
                defaults={
                    'value_chain': self.cleaned_data['value_chain'],
                    'existence_period': self.cleaned_data['existence_period'],
                    'facebook_link': self.cleaned_data['facebook_link'],
                    'twitter_link': self.cleaned_data['facebook_link'],
                    'instagram_link': self.cleaned_data['instagram_link'],
                    'linkedin_link': self.cleaned_data['linkedin_link'],
                    'whatsapp_business_link': self.cleaned_data['whatsapp_business_link']
                }
            )
            return business, created
        return None

    def save_covid_impact(self, business):
        if self.is_valid():
            impact, created = CovidImpact.objects.update_or_create(
                business=business,
                defaults={'impact': self.cleaned_data['impact']}
            )
            return impact, created
        return None

    def save_milestone(self, business):
        if self.is_valid():
            milestones = self.cleaned_data['milestones']
            milestone_objects = Milestone.objects.filter(id__in=milestones)
            for milestone in milestone_objects:
                milestone.businesses.add(business)
            return True

    def __init__(self, request=None, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        MILESTONES = [
            (milestone.id, milestone.milestone)
            for milestone in Milestone.objects.all()
        ]
        self.fields['milestones'].choices = MILESTONES