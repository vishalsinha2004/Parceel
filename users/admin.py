# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import User, DriverProfile

# Register the custom User
admin.site.register(User, UserAdmin)

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    # What columns show up in the admin list
    list_display = ('user', 'license_number', 'is_verified', 'is_online', 'view_documents')
    
    # Adds a filter sidebar to easily find unverified drivers
    list_filter = ('is_verified', 'is_online')
    
    # Adds a search bar to search by username or license number
    search_fields = ('user__username', 'user__phone_number', 'license_number')
    
    # Custom action to approve drivers quickly
    actions = ['approve_drivers']

    def approve_drivers(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected drivers have been successfully verified.")
    approve_drivers.short_description = "Approve and Verify selected drivers"

    # Function to show clickable links to the uploaded images
    def view_documents(self, obj):
        links = []
        if obj.photo:
            links.append(f'<a href="{obj.photo.url}" target="_blank">Photo</a>')
        if obj.aadhar_card:
            links.append(f'<a href="{obj.aadhar_card.url}" target="_blank">Aadhar</a>')
        if obj.license_image:
            links.append(f'<a href="{obj.license_image.url}" target="_blank">License</a>')
        
        # <-- Change format_html to mark_safe here
        return mark_safe(" | ".join(links)) if links else "No Documents Uploaded"
    
    view_documents.short_description = "Verification Docs"