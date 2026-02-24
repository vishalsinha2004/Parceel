from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # 1. THIS LINE MUST BE HERE
    driver_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        # 2. YOU MUST HAVE 'driver_name', 'rating', AND 'feedback' IN THIS LIST!
        fields = [
            'id', 'customer', 'driver', 'driver_name', 'pickup_location', 'dropoff_location', 
            'pickup_address', 'dropoff_address', 'distance_km', 'price', 'status', 
            'created_at', 'driver_lat', 'driver_lng', 'route_geometry',
            'rating', 'feedback'  
        ]

    # 3. THIS FUNCTION MUST BE HERE
    def get_driver_name(self, obj):
        if obj.driver:
            name = f"{obj.driver.first_name} {obj.driver.last_name}".strip()
            if name:
                return name
            return obj.driver.username 
        return None