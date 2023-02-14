from django.contrib import admin
from accounts.models import User, Coach


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    @admin.display(description='Special Id')
    def special_id(self, obj):
        return obj

    list_display = ['special_id', 'username',
                    'email', 'date_joined', 'is_active']
    search_fields = ['email', 'full_name', 'username', 'id']
    list_filter = ['is_active']


admin.site.register(Coach)
