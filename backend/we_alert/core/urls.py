from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SOSAlertViewSet, UnsafeAreaViewSet, CrimeViewSet,EmergencyContactViewSet, UserSettingsViewSet, SOSSessionViewSet

router=DefaultRouter()

router.register(r'sos-alerts',SOSAlertViewSet,basename='sosalert')
router.register(r'unsafe-areas',UnsafeAreaViewSet,basename='unsafearea')
router.register(r'crime-stats',CrimeViewSet,basename='crimestat')
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergencycontact')
router.register(r'user-settings', UserSettingsViewSet, basename='usersettings')
router.register(r'sos-sessions', SOSSessionViewSet, basename='sossession')

urlpatterns=[
    path('',include(router.urls)),
]