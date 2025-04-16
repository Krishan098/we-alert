from rest_framework import serializers
from .models import CustomUser,OTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','phone_number','is_active','is_staff','date_joined']
        read_only_fields=['is_active','is_staff','date_joined']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=OTP
        fields=['id','user','otp','created_at','expires_at','attempts','is_verified']
        read_only_fields=['created_at','expires_at','attempts','is_verified']

    # def validate(self, attrs):
    #     user=attrs.get('user')
    #     otp=attrs.get('otp')
    #     if not user:
    #         raise serializers.ValidationError("User is required")
    #     if not otp:
    #         raise serializers.ValidationError("OTP is required")
    #     return attrs
    