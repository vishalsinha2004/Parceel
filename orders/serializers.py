from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # --- ADDED: NEW FIELDS FOR NAMES AND PHONES ---
    driver_name = serializers.SerializerMethodField()
    driver_phone = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        # --- ADDED: MAKE SURE THE NEW FIELDS ARE IN THIS LIST ---
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone', 
            'driver', 'driver_name', 'driver_phone', 
            'pickup_location', 'dropoff_location', 
            'pickup_address', 'dropoff_address', 'distance_km', 'price', 'status', 
            'created_at', 'driver_lat', 'driver_lng', 'route_geometry',
            'rating', 'feedback'  
        ]

    # --- EXISTING DRIVER NAME ---
    def get_driver_name(self, obj):
        if obj.driver:
            name = f"{obj.driver.first_name} {obj.driver.last_name}".strip()
            if name:
                return name
            return obj.driver.username 
        return None

    # --- NEW: GET DRIVER PHONE ---
    def get_driver_phone(self, obj):
        if obj.driver and getattr(obj.driver, 'phone_number', None):
            return obj.driver.phone_number
        return None

    # --- NEW: GET CUSTOMER NAME ---
    def get_customer_name(self, obj):
        if obj.customer:
            name = f"{obj.customer.first_name} {obj.customer.last_name}".strip()
            if name:
                return name
            return obj.customer.username
        return None

    # --- NEW: GET CUSTOMER PHONE ---
    def get_customer_phone(self, obj):
        if obj.customer and getattr(obj.customer, 'phone_number', None):
            return obj.customer.phone_number
        return None