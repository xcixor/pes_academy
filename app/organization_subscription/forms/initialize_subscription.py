from django import forms


class InitiateSubscriptionForm(forms.Form):

    subscriber_email = forms.EmailField()
