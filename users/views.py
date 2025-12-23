from rest_framework.views import APIView
from rest_framework.response import Response  # <--- Make sure this is here!
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import DriverSignupSerializer, DriverProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DriverProfile
from rest_framework import permissions
from .serializers import UserSerializer

User = get_user_model()

class DriverSignupView(generics.CreateAPIView):
    serializer_class = DriverSignupSerializer
    parser_classes = (MultiPartParser, FormParser) 
    permission_classes = [permissions.AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful! Wait for Admin verification."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# backend/users/views.py

class CustomerSignupView(generics.CreateAPIView):
    # Use a standard User serializer or create a new one
    serializer_class = UserSerializer 
    permission_classes = [permissions.AllowAny] # Must be public

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DriverStatusView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({"error": "Username required"}, status=400)

        user = get_object_or_404(User, username=username)
        
        # Check if driver profile exists
        if hasattr(user, 'driver_profile'):
            return Response({
                "is_verified": user.driver_profile.is_verified,
                "is_active": user.is_active
            })
        else:
            return Response({"error": "Not a driver"}, status=400)
        
from rest_framework.permissions import IsAuthenticated

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    # NEW: Ensure only logged-in users can access these actions
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['post'], url_path='toggle_status')
    def toggle_status(self, request):
        # request.user is now guaranteed to be a real User object
        try:
            profile = DriverProfile.objects.get(user=request.user)
            profile.is_online = not profile.is_online
            profile.save()
            return Response({'is_online': profile.is_online})
        except DriverProfile.DoesNotExist:
            return Response({'error': 'Driver profile not found'}, status=404)