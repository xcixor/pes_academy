from django.contrib import admin
from application.models import (
    CallToAction, Application, ApplicationDocument, ApplicationReview,
    ApplicationScore, ApplicationPrompt, ApplicationComment)
from application.forms import CallToActionAdminForm


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    form = CallToActionAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}


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

    list_display = ['special_id', 'application_creator']

    inlines = [
        ApplicationDocumentInline, ApplicationReviewInline,
        ApplicationScoreInline, ApplicationPromptInline,
        ApplicationCommentInline]


@admin.register(ApplicationScore)
class ApplicationScoreAdmin(admin.ModelAdmin):

    list_display = ['score', 'application', 'reviewer']


@admin.register(ApplicationPrompt)
class ApplicationPromptAdmin(admin.ModelAdmin):

    list_display = ['reviewer', 'message']
