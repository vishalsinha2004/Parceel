from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DriverProfile

# Register the custom User
admin.site.register(User, UserAdmin)

# Register DriverProfile
@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'is_verified', 'is_online')