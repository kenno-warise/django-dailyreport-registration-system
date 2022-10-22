from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    
    list_display = (
        "user_no",
        "username",
        "active",
        "staff",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
    )
    filter_horizontal = ()
    ordering = ("user_no",)
    search_fields = ('user_no',)

    fieldsets = (
        (None, {'fields': ('user_no', 'password')}),
        ('Permissions', {'fields': ('staff','admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_no', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)

# Register your models here.
