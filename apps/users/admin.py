from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(admin.ModelAdmin):
    search_fields = ("email", "first_name", "last_name", "username")
    list_display = ("id", "first_name", "last_name", "email", "username", "is_active")
    list_editable = (
        "first_name",
        "last_name",
        "email",
        "username",
    )
    list_display_links = ("id",)


admin.site.register(get_user_model(), UserAdmin)
