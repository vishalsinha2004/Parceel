from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from .models import Order
from .serializers import OrderSerializer
from .utils import get_ride_details
from rest_framework.permissions import AllowAny
import razorpay
from django.conf import settings
client = razorpay.Client(auth=("rzp_test_RoJQxZI94ZIcLn", "t9gtZKjiRF6Qpggtt6pzuLuV"))
User = get_user_model()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny] # This allows requests without tokens

    def create(self, request, *args, **kwargs):
        # Extract coordinates from request data
        p_lng = request.data.get('pickup_longitude')
        p_lat = request.data.get('pickup_latitude')
        d_lng = request.data.get('dropoff_longitude')
        d_lat = request.data.get('dropoff_latitude')
        
        dist_km, price, route_geometry = get_ride_details((p_lng, p_lat), (d_lng, d_lat))

        # Create Razorpay Order
        razorpay_order = client.order.create({
            "amount": int(price * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        # Logic to handle user and save order
        user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        
        order = Order.objects.create(
            customer=user,
            pickup_location=Point(p_lng, p_lat, srid=4326),
            dropoff_location=Point(d_lng, d_lat, srid=4326),
            distance_km=dist_km,
            price=price,
            route_geometry=route_geometry,
            status='requested'
        )

        return Response({
            "id": order.id,
            "price": price,
            "razorpay_order_id": razorpay_order['id'],
            "route_geometry": route_geometry
        })

    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        # Verification logic for Razorpay Signature
        params_dict = {
            'razorpay_order_id': request.data.get('razorpay_order_id'),
            'razorpay_payment_id': request.data.get('razorpay_payment_id'),
            'razorpay_signature': request.data.get('razorpay_signature')
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            order = self.get_object()
            order.status = 'paid' # Update status upon success
            order.save()
            return Response({'status': 'Payment Verified'})
        except Exception:
            return Response({'error': 'Invalid Signature'}, status=400)