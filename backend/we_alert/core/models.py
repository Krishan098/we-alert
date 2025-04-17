from django.db import models
from django.contrib.auth.models import User
from authapp.models import CustomUser
from django.utils import timezone

class SOSAlert(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    latitude=models.FloatField()
    longitude=models.FloatField()
    is_resolved=models.BooleanField(default=False)

    def __str__(self):
        return f" SOSAlert by {self.user.phone_number} at {self.timestamp}"

class PastSOSAlert(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    latitude=models.FloatField()
    longitude=models.FloatField()
    is_resolved=models.BooleanField(default=False)

    def __str__(self):
        return f" PastSOSAlert by {self.user.phone_number} at {self.timestamp}"

class UnsafeArea(models.Model):
    name=models.CharField(max_length=255)
    latitude=models.FloatField()    
    longitude=models.FloatField()
    radius=models.FloatField(default=0.0) 
    created_at=models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.name} - {self.latitude}, {self.longitude}"
    
class CrimeStats(models.Model):
    state_ut=models.CharField(max_length=255)
    crime_head=models.CharField(max_length=255)
    year=models.IntegerField()
    total_cases=models.IntegerField()

    def __str__(self):
        return f"{self.state_ut} - {self.crime_head} - {self.year}" 


class EmergencyContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.phone_number}"

class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
    decoy_mode_enabled = models.BooleanField(default=False)
    voice_detection_enabled = models.BooleanField(default=True)
    gesture_detection_enabled = models.BooleanField(default=True)
    auto_sos_in_unsafe_area = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings for {self.user.phone_number}"

class SOSSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    current_latitude = models.FloatField()
    current_longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    activation_method = models.CharField(max_length=50, choices=[
        ('VOICE', 'Voice Detection'),
        ('GESTURE', 'Gesture Detection'),
        ('MANUAL', 'Manual Activation'),
        ('AUTO', 'Automatic - Unsafe Area')
    ])
    
    def __str__(self):
        return f"SOS Session by {self.user.phone_number} at {self.start_time}"
    
    def end_session(self):
        self.end_time = timezone.now()
        self.is_active = False
        self.save()
     
