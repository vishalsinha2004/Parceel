from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from .models import Order
from .serializers import OrderSerializer
from .utils import get_ride_details
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import razorpay
from django.conf import settings

client = razorpay.Client(auth=("rzp_test_SHfqRqFecIslSG", "LD8vhq3xQHjUhgD3NNFD9mhA"))
User = get_user_model()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny] # This allows requests without tokens
    authentication_classes = []

    # ==========================================
    # 1. DRIVER APP: ACCEPT RIDE
    # ==========================================
    @action(
        detail=True, 
        methods=['post'], 
        permission_classes=[IsAuthenticated], 
        authentication_classes=[JWTAuthentication]
    )
    def accept_ride(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'requested':
            return Response({"error": "Ride is already accepted or completed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to accepted and assign driver
        order.status = 'accepted'
        order.driver = request.user 
        order.save()
        
        return Response({
            "status": "accepted",
            "message": f"Ride {pk} has been accepted successfully"
        }, status=status.HTTP_200_OK)

    # ==========================================
    # 2. CUSTOMER APP: RATE DRIVER
    # ==========================================
    @action(detail=True, methods=['post'])
    def rate_driver(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'completed':
            return Response({"error": "Can only rate completed rides"}, status=status.HTTP_400_BAD_REQUEST)
        
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')

        if not rating:
            return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order.rating = int(rating)
            order.feedback = feedback
            order.save()
            return Response({
                "status": "success",
                "message": "Thank you! Rating submitted successfully."
            }, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid rating format"}, status=status.HTTP_400_BAD_REQUEST)

    # ==========================================
    # 3. CREATE RIDE / ORDER
    # ==========================================
    def create(self, request, *args, **kwargs):
        # 1. Use the correct keys sent from your frontend
        p_lng = request.data.get('pickup_lng') or request.data.get('pickup_longitude')
        p_lat = request.data.get('pickup_lat') or request.data.get('pickup_latitude')
        d_lng = request.data.get('dropoff_lng') or request.data.get('dropoff_longitude')
        d_lat = request.data.get('dropoff_lat') or request.data.get('dropoff_latitude')
        
        # Convert to float safely
        try:
            p_lng, p_lat = float(p_lng), float(p_lat)
            d_lng, d_lat = float(d_lng), float(d_lat)
        except (TypeError, ValueError):
            return Response({"error": "Invalid coordinates"}, status=400)

        dist_km, price, route_geometry = get_ride_details((p_lng, p_lat), (d_lng, d_lat))

        # 2. ENSURE MINIMUM PRICE (Fixes the BadRequestError)
        # Razorpay minimum is 100 paise (1 INR)
        if price < 1:
            price = 1.0 

        # 3. Create Razorpay Order
        try:
            razorpay_order = client.order.create({
                "amount": int(price * 100), # amount in paise
                "currency": "INR",
                "payment_capture": "1"
            })
        except Exception as e:
            return Response({"error": f"Razorpay error: {str(e)}"}, status=500)

        # 4. Save Order
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