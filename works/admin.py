from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .encryption import decryption
from .models import User, Work


class UserAdmin(BaseUserAdmin):
    
    list_display = (
        "user_no",
        # "username",
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
        (None, {'fields': ('user_no', 'username', 'password')}),
        ('Permissions', {'fields': ('staff','admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_no', 'username', 'password1', 'password2')}
        ),
    )


class WorkAdmin(admin.ModelAdmin):
    list_display = (
            "user_id",
            "date",
    )
    search_fields = ["user_id"]


admin.site.register(User, UserAdmin)
admin.site.register(Work, WorkAdmin)
# Register your models here.
