from django.contrib import admin
from django import forms
from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse,
    SubCriteriaItemFieldProperties)


admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


@admin.register(SubCriteriaItemFieldProperties)
class SubCriteriaItemFieldPropertiesAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'name', 'value']


class CustomSubCriteriaItemAdminForm(forms.ModelForm):
    class Meta:
        model = SubCriteriaItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomSubCriteriaItemAdminForm, self).__init__(*args, **kwargs)
        choices = [(index+1, index+1) for index, item in enumerate(SubCriteriaItem.objects.filter(
            criteria=self.instance.criteria))]
        self.fields['position_in_form'] = forms.ChoiceField()
        self.fields['position_in_form'].choices = choices
        self.fields['label'].initial = self.instance.label
        self.fields['criteria'].initial = self.instance.criteria
        self.fields['type'].initial = self.instance.type
        self.fields['position_in_form'].initial = self.instance.position_in_form


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
    form = CustomSubCriteriaItemAdminForm


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['application', 'sub_criteria_item', 'value']
