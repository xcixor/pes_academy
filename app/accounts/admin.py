from django.contrib import admin
from accounts.models import User, Coach
from application.models import (
    BusinessOrganization, Milestone, CovidImpact)


class BusinessOrganizationInline(admin.TabularInline):

    model = BusinessOrganization
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'date_joined']
    inlines = [BusinessOrganizationInline]


class CovidImpactInline(admin.TabularInline):

    model = CovidImpact
    extra = 0


class MilestoneInline(admin.TabularInline):

    model = Milestone
    extra = 0


@admin.register(BusinessOrganization)
class BusinessOrganizationAdmin(admin.ModelAdmin):

    list_display = ['organization_name', 'organization_owner']
    inlines = [CovidImpactInline]


admin.site.register(Coach)
