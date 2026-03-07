from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DriverProfile

User = get_user_model()


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['id', 'is_verified', 'is_online']
        read_only_fields = ['is_verified']

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
        profile_data = validated_data.pop('driver_profile', {})
        user = User.objects.create_user(**validated_data)

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
            is_verified=False,
             **profile_data # Default to Not Verified
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # FIX: Add 'phone_number' to this list so Django doesn't ignore it
        fields = ('id', 'username', 'email', 'phone_number', 'password', 'is_customer', 'is_driver')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # FIX: Ensure phone_number is extracted and saved
        phone_number = validated_data.pop('phone_number', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_customer=validated_data.get('is_customer', True),
            phone_number=phone_number # Save it to the database
        )
        return user