from django.contrib import admin
from eligibility.models import (
    ShortListGroup, ShortListGroupItems, BonusPoints)


class ShortListGroupItemsInline(admin.TabularInline):
    model = ShortListGroupItems


@admin.register(ShortListGroup)
class ShortListGroupItemsAdmin(admin.ModelAdmin):
    inlines = [ShortListGroupItemsInline]
    exclude = ('slug',)


@admin.register(BonusPoints)
class BonusPointsAdmin(admin.ModelAdmin):
    list_display = ['application', 'bonus']
