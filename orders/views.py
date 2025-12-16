from rest_framework import viewsets
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from .models import Order
from .serializers import OrderSerializer
from .utils import get_ride_details

User = get_user_model()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # 1. Get coordinates
        p_lat = float(self.request.data.get('pickup_lat'))
        p_lng = float(self.request.data.get('pickup_lng'))
        d_lat = float(self.request.data.get('dropoff_lat'))
        d_lng = float(self.request.data.get('dropoff_lng'))

        # 2. Create Points
        pickup_point = Point(p_lng, p_lat, srid=4326)
        dropoff_point = Point(d_lng, d_lat, srid=4326)

        # 3. Calculate Distance & Price
        dist_km, price = get_ride_details((p_lng, p_lat), (d_lng, d_lat))

        # 4. Handle User (If anonymous, assign to Admin for testing)
        user = self.request.user
        if not user.is_authenticated:
            user = User.objects.filter(is_superuser=True).first()

        # 5. Save with Dummy Addresses
        serializer.save(
            customer=user,
            pickup_location=pickup_point,
            dropoff_location=dropoff_point,
            distance_km=dist_km,
            price=price,
            pickup_address="Map Selection",  # Dummy text for now
            dropoff_address="Map Selection"
        )