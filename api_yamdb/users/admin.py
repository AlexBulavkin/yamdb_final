from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Отражение модели User в админке."""
    list_display = ('id', 'username', 'email', 'role', 'bio')


admin.site.register(User, UserAdmin)
