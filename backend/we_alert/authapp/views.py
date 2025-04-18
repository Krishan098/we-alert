from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from .models import CustomUser, OTP
from .serializers import UserSerializer, OTPSerializer
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client
from datetime import timedelta
from rest_framework.decorators import api_view,permission_classes
import random
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_iser(request):
    phone_number=request.data.get("phone_number")
    name=request.data.get("name")
    email=request.data.get("email")

    if not phone_number:
        return Response({"error":"Phone Number is required"},status=status.HTTP_400_BAD_REQUEST)
    user_exists = CustomUser.objects.filter(phone_number=phone_number).exists()
    
    if user_exists:
        # Update existing user with new information
        user = CustomUser.objects.get(phone_number=phone_number)
        if name:
            user.name = name
        if email:
            user.email = email
        user.save()
    else:
        # Create new user
        user = CustomUser.objects.create(
            phone_number=phone_number,
            name=name,
            email=email
        )



class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create or get the user
            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
            
            # Generate OTP
            code = str(random.randint(100000, 999999))
            
            # Set expiration and create OTP record
            expires_at = timezone.now() + timedelta(minutes=4)
            otp = OTP.objects.create(user=user, otp=code, expires_at=expires_at)
            
            # Debug environment variables
            print(f"TWILIO_ACCOUNT_SID: {settings.TWILIO_ACCOUNT_SID}")
            print(f"TWILIO_NUMBER: {settings.TWILIO_NUMBER}")
            
            try:
                # Send SMS via Twilio
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"Your OTP is {code}",
                    from_=settings.TWILIO_NUMBER,
                    to=phone_number
                )
                print(f"Twilio message SID: {message.sid}")
            except Exception as twilio_error:
                # Log the Twilio error but don't fail the request
                print(f"Twilio error: {str(twilio_error)}")
                # We'll still return success since the OTP was created in our system
            
            # Return success response
            return Response(
                {"message": "OTP sent successfully to your Number", "is_new_user": created},
                status=status.HTTP_200_OK
            )
                
        except Exception as e:
            print(f"Error in SendOTPView: {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class VerifyOTPView(APIView):
    def post(self,request):
        phone_number=request.data.get('phone_number')
        code=request.data.get('otp')
        try:
            user=CustomUser.objects.get(phone_number=phone_number)
            otp=OTP.objects.filter(user=user).latest('created_at')

            if otp.attempts>=3:
                return Response({"error":"Maximum attempts exceeded"},status=status.HTTP_403_FORBIDDEN)
            if not otp.is_valid():
                return Response({"error":"OTP expired"},status=status.HTTP_400_BAD_REQUEST)
            if otp.otp==code:
                otp.is_verified=True
                otp.save()
                refresh = RefreshToken.for_user(user)
                return Response({"message":"OTP verified successfully",
                    "token":{
                        "refresh":str(refresh),
                        "access":str(refresh.access_token)
                    },
                    "user":{
                        "phone_number":user.phone_number,
                        "name":user.name if user.name else None
                    }             },status=status.HTTP_200_OK)
            else:
                otp.attempts+=1
                otp.save()
                return Response({"error":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error":"User does not exist"},status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return Response({"error":"OTP does not exist"},status=status.HTTP_404_NOT_FOUND)

