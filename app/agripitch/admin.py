from django.contrib import admin
from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse)


admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['application', 'sub_criteria_item', 'value']
