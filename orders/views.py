from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from .models import Order
from .serializers import OrderSerializer
from .utils import get_ride_details

User = get_user_model()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # 1. Get coordinates
        p_lat = float(request.data.get('pickup_lat'))
        p_lng = float(request.data.get('pickup_lng'))
        d_lat = float(request.data.get('dropoff_lat'))
        d_lng = float(request.data.get('dropoff_lng'))

        # 2. Get OSRM Data (Price + Route Shape)
        dist_km, price, route_geometry = get_ride_details((p_lng, p_lat), (d_lng, d_lat))

        # 3. Handle User
        user = request.user
        if not user.is_authenticated:
            user = User.objects.filter(is_superuser=True).first()

        # 4. ROBUST ADDRESS HANDLING (The Fix)
        # This checks: If data is None OR Empty String -> Use "Map Selection"
        pickup_addr = request.data.get('pickup_address') or "Map Selection"
        dropoff_addr = request.data.get('dropoff_address') or "Map Selection"

        # 5. Save the Order
        order = Order.objects.create(
            customer=user,
            pickup_location=Point(p_lng, p_lat, srid=4326),
            dropoff_location=Point(d_lng, d_lat, srid=4326),
            distance_km=dist_km,
            price=price,
            pickup_address=pickup_addr,   # <-- Safe Value
            dropoff_address=dropoff_addr, # <-- Safe Value
            status='requested'
        )

        return Response({
            "id": order.id,
            "status": order.status,
            "distance_km": dist_km,
            "price": price,
            "route_geometry": route_geometry
        })

    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'requested':
            return Response({'error': 'Ride already taken!'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'accepted'
        order.save()
        
        return Response({'status': 'Ride Accepted', 'order_id': order.id})