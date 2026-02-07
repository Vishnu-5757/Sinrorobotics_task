from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task

# This tells Django how to display your custom user in the built-in admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'manager', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'manager')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'manager')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)