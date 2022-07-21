from django.contrib import admin
from agripitch.models import (
    AFDBApplication, Competition, ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaDocumentPrompt, SubCriteriaInputFieldPrompt,
    SubCriteriaTextFieldInputPrompt)

admin.site.register(AFDBApplication)
admin.site.register(ShortList)
admin.site.register(SubCriteriaItemChoice)


@admin.register(Competition)
class CallToActionAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['tagline', 'deadline', 'available_for_applications']


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
