from rest_framework import serializers
from .models import SOSAlert, PastSOSAlert, UnsafeArea, CrimeStats,EmergencyContact,UserSettings,SOSSession

class SOSAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model=SOSAlert
        fields=['id','user','timestamp','latitude','longitude','is_resolved']
        read_only_fields=['id','user','timestamp','is_resolved']

class PastSOSAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model=PastSOSAlert
        fields=['id','user','timestamp','latitude','longitude','is_resolved']
        read_only_fields=['id','user','timestamp','is_resolved']

class UnsafeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=UnsafeArea
        fields=['id','name','latitude','longitude','radius','created_at']
        read_only_fields=['id','created_at']

class CrimeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CrimeStats
        fields=['id','state_ut','crime_head','year','total_cases']

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'phone_number', 'relationship']
        
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['id', 'decoy_mode_enabled', 'voice_detection_enabled', 'gesture_detection_enabled', 'auto_sos_in_unsafe_area']
        
class SOSSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOSSession
        fields = ['id', 'user', 'start_time', 'end_time', 'current_latitude', 'current_longitude', 'is_active', 'activation_method']
        read_only_fields = ['id', 'user', 'start_time', 'end_time']




