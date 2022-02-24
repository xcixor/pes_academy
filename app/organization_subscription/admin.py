from django.contrib import admin
from organization_subscription.models import OrganizationSubscription, Subscription


class SubscribersInline(admin.TabularInline):

    model = Subscription
    extra = 0


@admin.register(OrganizationSubscription)
class OrganizationSubscriptionAdmin(admin.ModelAdmin):

    inlines = [SubscribersInline]


admin.site.register(Subscription)
