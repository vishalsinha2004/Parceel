from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DriverProfile

User = get_user_model()

class DriverSignupSerializer(serializers.ModelSerializer):
    # Explicitly define file fields for the upload form
    photo = serializers.ImageField(write_only=True, required=True)
    aadhar_card = serializers.ImageField(write_only=True, required=True)
    license_image = serializers.ImageField(write_only=True, required=True)
    license_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'photo', 'aadhar_card', 'license_image', 'license_number']

    def create(self, validated_data):
        # 1. Pop out driver-specific data
        photo = validated_data.pop('photo')
        aadhar = validated_data.pop('aadhar_card')
        license_img = validated_data.pop('license_image')
        license_num = validated_data.pop('license_number')
        password = validated_data.pop('password')

        # 2. Create the base User
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_driver = True  # Mark as driver
        user.save()

        # 3. Create the Driver Profile with files
        DriverProfile.objects.create(
            user=user,
            photo=photo,
            aadhar_card=aadhar,
            license_image=license_img,
            license_number=license_num,
            is_verified=False # Default to Not Verified
        )
        return user