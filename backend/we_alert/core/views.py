from django.shortcuts import render
from rest_framework import generics,permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SOSAlert, PastSOSAlert, UnsafeArea, CrimeStats,EmergencyContact,UserSettings,SOSSession
from .serializers import SOSAlertSerializer, PastSOSAlertSerializer, UnsafeAreaSerializer, CrimeStatsSerializer,SOSSessionSerializer,EmergencyContactSerializer,UserSettingsSerializer
from django.utils import timezone
from rest_framework.decorators import action
from twilio.rest import Client
from django.conf import settings

class SOSAlertViewSet(viewsets.ModelViewSet):
    queryset=SOSAlert.objects.all()
    serializer_class=SOSAlertSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UnsafeAreaViewSet(viewsets.ModelViewSet):
    queryset=UnsafeArea.objects.all()
    serializer_class=UnsafeAreaSerializer
    permission_classes=[permissions.IsAuthenticated]


class CrimeViewSet(viewsets.ModelViewSet):
    queryset=CrimeStats.objects.all()
    serializer_class=CrimeStatsSerializer
    permission_classes=[permissions.AllowAny]    

class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)
    
    def get_object(self):
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        return settings
class SOSSessionViewSet(viewsets.ModelViewSet):
    serializer_class = SOSSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SOSSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)
        self.notify_emergency_contacts(session)
        
        return session
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        session = self.get_object()
        if session.is_active:
            session.end_session()
            return Response({"message": "SOS session ended"}, status=status.HTTP_200_OK)
        return Response({"message": "Session already ended"}, status=status.HTTP_400_BAD_REQUEST)
    
    def notify_emergency_contacts(self, session):
        contacts=EmergencyContactSerializer.objects.filter(user=session.user)
        if contacts.exists():
            client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
            message_body=(
                f"EMERGENCY ALERT: {session.user.phone_number} has triggered an SOS alert. "
                f"They are located at coordinates: {session.current_latitude}, {session.current_longitude}. "
                f"Please check on them immediately."
            )
            for contact in contacts:
                try:
                    message = client.messages.create(
                        body=message_body,
                        from_=settings.TWILIO_NUMBER,
                        to=contact.phone_number
                    )
                except Exception as e:
                    
                    print(f"Failed to send message to {contact.phone_number}: {str(e)}")

