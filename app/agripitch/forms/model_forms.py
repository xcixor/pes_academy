from django import forms
from agripitch.models import SubCriteriaItem


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
