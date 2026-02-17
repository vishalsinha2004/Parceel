from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'driver', 'pickup_location', 'dropoff_location', 
            'pickup_address', 'dropoff_address', 'distance_km', 'price', 'status', 
            'created_at', 'driver_lat', 'driver_lng', 'route_geometry'
            # Add 'razorpay_order_id' here if you added it to models.py
        ]