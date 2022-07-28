from django.contrib import admin
from agripitch.forms import CustomSubCriteriaItemAdminForm

from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse,
    SubCriteriaItemFieldProperties, ValidatorType,
    SubCriteriaItemValidators, FileExtension,
    SubCriteriaItemFileExtension)


admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)
admin.site.register(ValidatorType)
admin.site.register(SubCriteriaItemValidators)
admin.site.register(FileExtension)
admin.site.register(SubCriteriaItemFileExtension)


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


@admin.register(SubCriteriaItemFieldProperties)
class SubCriteriaItemFieldPropertiesAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'name', 'value']


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
    form = CustomSubCriteriaItemAdminForm


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['application', 'sub_criteria_item', 'value']
