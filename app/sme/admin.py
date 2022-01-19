from django.contrib import admin
from sme.models import Application
from sme.forms import ApplicationAdminForm


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}
