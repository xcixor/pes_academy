from django.contrib import admin
from agripitch.forms import (
    CustomSubCriteriaItemAdminForm)

from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse,
    SubCriteriaItemFieldProperties, SubCriteriaItemDocumentResponse)


admin.site.register(ShortList)


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'application', 'value']


@admin.register(SubCriteriaItemDocumentResponse)
class SubCriteriaItemDocumentResponseAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'application', 'document']


@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'shortlist']


class SubCriteriaItemFieldPropertiesInline(admin.TabularInline):

    model = SubCriteriaItemFieldProperties
    extra = 0


class SubCriteriaItemChoiceInline(admin.TabularInline):

    model = SubCriteriaItemChoice
    extra = 0


class SubCriteriaItemDocumentResponseInline(admin.TabularInline):

    model = SubCriteriaItemDocumentResponse
    extra = 0


class SubCriteriaItemResponseInline(admin.TabularInline):

    model = SubCriteriaItemResponse
    extra = 0


@admin.register(SubCriteriaItem)
class SubCriteriaItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'criteria']
    form = CustomSubCriteriaItemAdminForm
    inlines = [
        SubCriteriaItemFieldPropertiesInline,
        SubCriteriaItemResponseInline,
        SubCriteriaItemDocumentResponseInline,
        SubCriteriaItemChoiceInline, ]
