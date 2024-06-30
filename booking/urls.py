
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, SlotViewSet, BookingViewSet, ZoomIntegrationViewSet

app_name = 'booking'

router = DefaultRouter()

router.register(r'slots', SlotViewSet)
router.register(r'bookings', BookingViewSet)  # Typically pluralize for consistency
router.register(r'zoom', ZoomIntegrationViewSet, basename='zoom')  # Ensure basename is singular

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
]

