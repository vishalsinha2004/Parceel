# orders/admin.py
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns to display for quick overview
    list_display = ('id', 'customer', 'driver', 'status', 'price', 'created_at')
    
    # Filter by status (e.g., to quickly find 'cancelled' or 'in_transit' orders)
    list_filter = ('status', 'created_at')
    
    # Search bar to find specific orders when a customer calls/emails
    search_fields = ('customer__username', 'driver__username', 'id')
    
    # Organize the form view cleanly into sections
    fieldsets = (
        ('Ride Details', {
            'fields': ('customer', 'driver', 'status', 'price', 'distance_km')
        }),
        ('Addresses', {
            'fields': ('pickup_address', 'dropoff_address')
        }),
        ('Customer Support (Feedback)', {
            'fields': ('rating', 'feedback')
        }),
        ('Geospatial Data (Advanced)', {
            'classes': ('collapse',), # Hides this section by default to keep UI clean
            'fields': ('pickup_location', 'dropoff_location', 'driver_lat', 'driver_lng', 'route_geometry')
        }),
    )