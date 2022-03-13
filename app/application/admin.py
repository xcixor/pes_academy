from django.contrib import admin
from application.models import (
    CallToAction, Application, ApplicationDocument, ApplicationReview)
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
    extra = 1


class ApplicationReviewInline(admin.TabularInline):

    model = ApplicationReview
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = ['special_id', 'application_creator']

    inlines = [ApplicationDocumentInline, ApplicationReviewInline]
