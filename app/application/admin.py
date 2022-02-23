from django.contrib import admin
from application.models import CallToAction
from application.forms import CallToActionAdminForm


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    form = CallToActionAdminForm
    list_display = ['tagline', 'deadline', 'available_for_applications']
    prepopulated_fields = {'slug': ('tagline',)}
