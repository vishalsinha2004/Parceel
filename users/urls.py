from django.urls import path
from .views import DriverSignupView
from .views import DriverStatusView


urlpatterns = [
    path('signup/driver/', DriverSignupView.as_view(), name='driver-signup'),
    path('status/', DriverStatusView.as_view(), name='driver-status'),
]