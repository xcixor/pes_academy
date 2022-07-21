from django.contrib import admin
from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice)


admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
