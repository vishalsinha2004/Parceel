from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # MAKE SURE ALL THESE ARE PRESENT
        fields = [
            'id', 'customer', 'driver', 'pickup_location', 'dropoff_location', 
            'pickup_address', 'dropoff_address', 'distance_km', 'price', 'status', 'created_at', 'driver_lat', 'driver_lng', 'route_geometry'
        ]