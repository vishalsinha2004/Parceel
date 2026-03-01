# backend/users/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from .views import DriverSignupView, DriverStatusView, DriverProfileViewSet
from .views import CustomerSignupView

# Define the Public Login View correctly
class PublicTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

router = DefaultRouter()
router.register(r'driver_profile', DriverProfileViewSet, basename='driverprofile')

urlpatterns = [
    # JWT Auth
    path('login/', PublicTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Driver Endpoints
    path('signup/driver/', DriverSignupView.as_view(), name='driver-signup'),
    path('status/', DriverStatusView.as_view(), name='driver-status'),
    

    path('signup/', CustomerSignupView.as_view(), name='customer-signup'),
    # Router URLs (includes toggle_status)
    path('', include(router.urls)),
]