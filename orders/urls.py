from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()

# ---> FIX: Add basename='rides' right here! <---
router.register(r'rides', OrderViewSet, basename='rides')

urlpatterns = [
    path('', include(router.urls)),
]