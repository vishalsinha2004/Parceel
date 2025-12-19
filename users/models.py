from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as geomodels  # PostGIS magic
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
    
    # --- EXISTING FIELDS ---
    license_number = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False) # Admin approves this
    is_online = models.BooleanField(default=False)   # Toggle for "Ready to work"
    
    # --- NEW: VERIFICATION DOCUMENTS ---
    # We use ImageField to store the actual files
    photo = models.ImageField(upload_to='driver_photos/', blank=True, null=True)
    aadhar_card = models.ImageField(upload_to='driver_docs/', blank=True, null=True)
    license_image = models.ImageField(upload_to='driver_docs/', blank=True, null=True)

    # --- LIVE LOCATION ---
    current_location = geomodels.PointField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"