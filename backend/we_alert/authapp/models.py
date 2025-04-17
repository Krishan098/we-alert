from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
import random

class CustomUserManager(BaseUserManager):
    def create_user(self,phone_number,password=None,**extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user=self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,phone_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(phone_number,password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    phone_number=models.CharField(max_length=15,unique=True)
    name=models.CharField(max_length=100,blank=True)
    email=models.EmailField(blank=True,max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.now)

    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()

    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    attempts=models.IntegerField(default=0)
    is_verified=models.BooleanField(default=False)

    def  is_valid(self):
        return timezone.now() < self.expires_at and not self.is_verified 
    def __str__(self):
        return f"OTP for {self.user.phone_number}"
           

    

