from django.contrib import admin
from eligibility.models import ShortListGroup, ShortListGroupItems


class ShortListGroupItemsInline(admin.TabularInline):
    model = ShortListGroupItems


@admin.register(ShortListGroup)
class ShortListGroupItemsAdmin(admin.ModelAdmin):
    inlines = [ShortListGroupItemsInline]
    exclude = ('slug',)
