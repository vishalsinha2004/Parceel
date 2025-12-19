from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DriverSignupView
from .views import DriverStatusView
from .views import DriverSignupView, DriverStatusView, DriverProfileViewSet

from .views import DriverProfileViewSet
router = DefaultRouter()
router.register(r'driver_profile', DriverProfileViewSet, basename='driver_profile')
urlpatterns = [
    path('signup/driver/', DriverSignupView.as_view(), name='driver-signup'),
    path('status/', DriverStatusView.as_view(), name='driver-status'),
    path('', include(router.urls)),
]