from django import forms
from application.models import BusinessOrganization, Milestone, CovidImpact
from accounts.models import User
from organization_subscription.models import Subscription
from application.services.redis_caching import (
    get_draft_application_data_from_redis_cache)
from common.utils.common_queries import get_application


class ApplicationForm(forms.Form):

    full_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'text draftable', 'placeholder': 'Full Name'}))
    age = forms.ChoiceField(
        choices=User.AGE_CHOICES, widget=forms.RadioSelect)
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.RadioSelect)
    preferred_language = forms.ChoiceField(
        widget=forms.RadioSelect, choices=User.LANGUAGE_CHOICES)
    organization_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'text draftable', 'placeholder': 'Organization Name'}))
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable', 'placeholder': 'Facebook Page Link'}))
    twitter_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable', 'placeholder': 'Twitter Link'}))
    instagram_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable', 'placeholder': 'Instagram Page'}))
    linkedin_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable', 'placeholder': 'LinkedIn Page'}))
    whatsapp_business_link = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'text draftable', 'placeholder': 'Whatsapp Business Link'}))
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
        attrs={'class': 'text draftable', 'placeholder': 'Covid 19 Impact'}))
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
                username='test_user01',
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

    def update_application(self, user):
        application, msg = get_application(user)
        application.status = 'step_two'
        application.save()

    def __init__(self, request=None, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        MILESTONES = [
            (milestone.id, milestone.milestone)
            for milestone in Milestone.objects.all()
        ]
        self.fields['milestones'].choices = MILESTONES
        application, msg = get_application(request.user)
        if application:
            data = get_draft_application_data_from_redis_cache(application.pk)
            self.fields['age'].initial = data.get('age', None)
            self.fields['full_name'].initial = data.get('full_name', None)
            self.fields['preferred_language'].initial = data.get(
                'preferred_language', None)
            self.fields['gender'].initial = data.get('gender', None)
            self.fields['organization_name'].initial = data.get(
                'organization_name', None)
            self.fields['facebook_link'].initial = data.get(
                'facebook_link', None)
            self.fields['twitter_link'].initial = data.get(
                'twitter_link', None)
            self.fields['instagram_link'].initial = data.get(
                'instagram_link', None)
            self.fields['linkedin_link'].initial = data.get(
                'linkedin_link', None)
            self.fields['whatsapp_business_link'].initial = data.get(
                'whatsapp_business_link', None)
            self.fields['value_chain'].initial = data.get(
                'value_chain', None)
            self.fields['existence_period'].initial = data.get(
                'existence_period', None)
            self.fields['stage'].initial = data.get(
                'stage', None)
            self.fields['impact'].initial = data.get(
                'impact', None)
