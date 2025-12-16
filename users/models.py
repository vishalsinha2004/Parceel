from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as geomodels  # This is the PostGIS magic
from django.db import models

class User(AbstractUser):
    # Roles to distinguish users
    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True)

    def __str__(self):
        return self.username

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    
    # Driver Specifics
    license_number = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False) # Admin approves this
    is_online = models.BooleanField(default=False)   # Toggle for "Ready to work"
    
    # LIVE LOCATION (This is why we needed PostGIS!)
    # We store Longitude and Latitude here
    current_location = geomodels.PointField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return f"Driver: {self.user.username}"  