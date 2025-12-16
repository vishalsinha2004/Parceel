from django.contrib.gis.db import models as geomodels
from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_orders')
    
    # Locations (Using PostGIS PointField)
    pickup_location = geomodels.PointField(srid=4326)  # Stores (Longitude, Latitude)
    dropoff_location = geomodels.PointField(srid=4326)
    pickup_address = models.TextField()
    dropoff_address = models.TextField()
    
    # Money & Math
    distance_km = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"