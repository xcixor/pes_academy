from django.contrib import admin
from agripitch.models import (
    AFDBApplication, Competition, ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaDocumentPrompt, SubCriteriaInputFieldPrompt,
    SubCriteriaTextFieldInputPrompt, SubCriteriaSelectFieldInputPrompt,
    SubCriteriaSelectFieldInputPromptChoice, SubCriteriaRadioFieldInputPrompt,
    SubCriteriaRadioFieldInputPromptOption)

admin.site.register(AFDBApplication)
admin.site.register(ShortList)
admin.site.register(CriteriaItem)


@admin.register(Competition)
class CallToActionAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['tagline', 'deadline', 'available_for_applications']
