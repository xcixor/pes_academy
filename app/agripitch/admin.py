from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline
from agripitch.forms import (
    CustomSubCriteriaItemAdminForm, PartnerLogoAdminForm,
    SubCriteriaItemFieldPropertiesAdminForm, CustomCriteriaItemAdminForm)

from agripitch.models import (
    ShortList, CriteriaItem,
    SubCriteriaItem, SubCriteriaItemChoice, SubCriteriaItemResponse,
    SubCriteriaItemFieldProperties, SubCriteriaItemDocumentResponse,
    PartnerLogo)


@admin.register(SubCriteriaItemChoice)
class SubCriteriaItemChoiceAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


@admin.register(ShortList)
class ShortListAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


@admin.register(SubCriteriaItemResponse)
class SubCriteriaItemResponseAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'application', 'value']
    list_filter = ['sub_criteria_item', 'application']


@admin.register(SubCriteriaItemDocumentResponse)
class SubCriteriaItemDocumentResponseAdmin(admin.ModelAdmin):
    list_display = ['sub_criteria_item', 'application', 'document']
    list_filter = ['sub_criteria_item', 'application']


@admin.register(CriteriaItem)
class CriteriaItemAdmin(TranslatableAdmin):
    list_display = ['label', 'shortlist']
    form = CustomCriteriaItemAdminForm
    inlines = [TranslationInline]


class SubCriteriaItemFieldPropertiesInline(admin.TabularInline):

    model = SubCriteriaItemFieldProperties
    extra = 0
    form = SubCriteriaItemFieldPropertiesAdminForm


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
class SubCriteriaItemAdmin(TranslatableAdmin):
    list_display = ['label', 'position_in_form', 'criteria']
    list_filter = ['criteria', ]
    form = CustomSubCriteriaItemAdminForm
    inlines = [
        SubCriteriaItemFieldPropertiesInline,
        SubCriteriaItemChoiceInline, TranslationInline]


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    form = PartnerLogoAdminForm
