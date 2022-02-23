from django.contrib import admin
from organization_subscription.models import OrganizationSubscription
from accounts.models import User


class SubscribersInline(admin.TabularInline):

    model = User
    extra = 0


# @admin.register(OrganizationSubscription)
# class OrganizationSubscriptionAdmin(admin.ModelAdmin):

#     inlines = [SubscribersInline]

admin.site.register(OrganizationSubscription)

