from django.contrib import admin
from application.models import Application
from application.forms import ApplicationAdminForm


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}
