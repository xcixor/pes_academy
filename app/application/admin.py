from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline
from application.models import (
    CallToAction, Application, ApplicationDocument, ApplicationReview,
    ApplicationScore, ApplicationPrompt, ApplicationComment,
    CarouselImage, QuestionComment)
from application.forms import CallToActionAdminForm


admin.site.register(CarouselImage)
admin.site.register(QuestionComment)


@admin.register(CallToAction)
class CallToActionAdmin(TranslatableAdmin):
    form = CallToActionAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}
    inlines = [TranslationInline]


@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'reviewer']
    search_fields = ['application', 'reviewer__email',
                     'reviewer__pk', 'reviewer__id']


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):

    list_display = ['application', 'creator', 'reviewer', 'document_name', ]
    search_fields = ['application__application_creator__id',
                     'application__application_creator__email', 'application__slug']


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
    list_filter = ['stage', 'is_in_review', 'disqualified']
    search_fields = ['application_creator__email',
                     'application_creator__id', 'application_creator__pk']


@admin.register(ApplicationScore)
class ApplicationScoreAdmin(admin.ModelAdmin):

    list_display = ['score', 'application', 'reviewer']


@admin.register(ApplicationPrompt)
class ApplicationPromptAdmin(admin.ModelAdmin):

    list_display = ['reviewer', 'message']
