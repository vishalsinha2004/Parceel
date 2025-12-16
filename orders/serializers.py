from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        # VISHAL: We added 'pickup_location' and 'dropoff_location' here.
        # This tells Django: "Don't ask the frontend for these, we will calculate them."
        read_only_fields = (
            'customer', 'price', 'distance_km', 'status', 'created_at',
            'pickup_address', 'dropoff_address',
            'pickup_location', 'dropoff_location'
        )