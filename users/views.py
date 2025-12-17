from rest_framework.views import APIView
from rest_framework.response import Response  # <--- Make sure this is here!
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DriverSignupSerializer

User = get_user_model()

class DriverSignupView(generics.CreateAPIView):
    serializer_class = DriverSignupSerializer
    parser_classes = (MultiPartParser, FormParser) 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful! Wait for Admin verification."}, status=status.HTTP_201_CREATED)
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