from django.contrib import admin
from django import forms
from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse)


admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


class CustomForm(forms.ModelForm):
    class Meta:
        model = SubCriteriaItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        choices = [(index+1, index+1) for index, item in enumerate(SubCriteriaItem.objects.filter(
            criteria=self.instance.criteria))]
        choices.insert(0, [0, 0])
        self.fields['position_in_form'] = forms.ChoiceField(
            help_text='Do not start at 0, the zeroth index helps you incase you have a duplicate error')
        self.fields['position_in_form'].choices = choices
        print(self.fields['position_in_form'].choices)
        self.fields['label'].initial = self.instance.label
        self.fields['criteria'].initial = self.instance.criteria
        self.fields['type'].initial = self.instance.type
        self.fields['position_in_form'].initial = self.instance.position_in_form


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
    form = CustomForm


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['application', 'sub_criteria_item', 'value']
