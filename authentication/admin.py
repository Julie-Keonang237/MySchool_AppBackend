from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'user_name', 'user_surname', 'is_verified', 'is_active', 'is_admin']
    list_filter = ['is_verified', 'is_active', 'is_admin', 'role']
    search_fields = ['email', 'user_name', 'user_surname']
    
    readonly_fields = ('created_at', 'updated_at')   # 👈 added
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_name', 'user_surname', 'telephone', 'sexe')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_admin', 'is_online', 'role')}),
        ('Important dates', {'fields': ('last_login', 'email_verified_at', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'user_surname', 'telephone', 'role', 'sexe', 'password1', 'password2'),
        }),
    )
    
    ordering = ['email']
    actions = ['verify_users']
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
    verify_users.short_description = "Mark selected users as verified"

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)