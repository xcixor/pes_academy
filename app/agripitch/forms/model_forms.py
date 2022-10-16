from django import forms
from agripitch.models import (
    SubCriteriaItem, PartnerLogo, CriteriaItem)


class CustomSubCriteriaItemAdminForm(forms.ModelForm):

    class Meta:
        model = SubCriteriaItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomSubCriteriaItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            choices = [
                (index+1, index+1) for index, item in enumerate(
                    SubCriteriaItem.objects.filter(criteria=self.instance.criteria))]
            self.fields['position_in_form'] = forms.ChoiceField()
            self.fields['position_in_form'].choices = choices
            self.fields['label'].initial = self.instance.label
            self.fields['criteria'].initial = self.instance.criteria
            self.fields['type'].initial = self.instance.type
            self.fields['position_in_form'].initial = self.instance.position_in_form
        else:
            self.fields['position_in_form'].widget = forms.HiddenInput()


class PartnerLogoAdminForm(forms.ModelForm):
    class Meta:
        model = PartnerLogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PartnerLogoAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            choices = [
                (index+1, index+1) for index in range(
                    0, PartnerLogo.objects.count())]
            self.fields['position'] = forms.ChoiceField()
            self.fields['position'].choices = choices
        else:
            self.fields['position'].widget = forms.HiddenInput()


class CustomCriteriaItemAdminForm(forms.ModelForm):

    class Meta:
        model = CriteriaItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomCriteriaItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            choices = [
                (index+1, index+1) for index, item in enumerate(
                    CriteriaItem.objects.all())
            ]
            self.fields['position_in_form'] = forms.ChoiceField()
            self.fields['position_in_form'].choices = choices
            self.fields['label'].initial = self.instance.label
            self.fields['shortlist'].initial = self.instance.shortlist
            self.fields['position_in_form'].initial = self.instance.position_in_form
        else:
            self.fields['position_in_form'].widget = forms.HiddenInput()
