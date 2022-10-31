from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline
from application.models import (
    CallToAction, Application, ApplicationDocument, ApplicationReview,
    ApplicationScore, ApplicationPrompt, ApplicationComment,
    CarouselImage)
from application.forms import CallToActionAdminForm


admin.site.register(CarouselImage)


@admin.register(CallToAction)
class CallToActionAdmin(TranslatableAdmin):
    form = CallToActionAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}
    inlines = [TranslationInline]


@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'reviewer']


class ApplicationDocumentInline(admin.TabularInline):

    model = ApplicationDocument
    extra = 0


class ApplicationPromptInline(admin.TabularInline):

    model = ApplicationPrompt
    extra = 0


class ApplicationScoreInline(admin.TabularInline):

    model = ApplicationScore
    extra = 0


class ApplicationReviewInline(admin.TabularInline):

    model = ApplicationReview
    extra = 0


class ApplicationCommentInline(admin.TabularInline):

    model = ApplicationComment
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = ['special_id', 'application_creator', 'created']
    list_filter = ['stage']
    search_fields = ['application_creator__email', 'slug']


@admin.register(ApplicationScore)
class ApplicationScoreAdmin(admin.ModelAdmin):

    list_display = ['score', 'application', 'reviewer']


@admin.register(ApplicationPrompt)
class ApplicationPromptAdmin(admin.ModelAdmin):

    list_display = ['reviewer', 'message']
