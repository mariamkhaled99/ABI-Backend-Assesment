from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from booking.models.booking_models import Slot, Booking
from booking.serializers import SlotSerializer, BookingSerializer
import requests
from django.http import Http404
from django.conf import settings
from django.db import transaction
from booking.models.user_models import CustomUser
import jwt
import time

# Zoom Configuration
ACCOUNT_ID = settings.ACCOUNT_ID
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET





@extend_schema_view(
    list=extend_schema(tags=['Slots']),
    retrieve=extend_schema(tags=['Slots']),
    create=extend_schema(tags=['Slots']),
    update=extend_schema(tags=['Slots']),
    partial_update=extend_schema(tags=['Slots']),
    destroy=extend_schema(tags=['Slots']),
)
class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['Bookings']),
    retrieve=extend_schema(tags=['Bookings']),
    create=extend_schema(tags=['Bookings']),
    update=extend_schema(tags=['Bookings']),
    partial_update=extend_schema(tags=['Bookings']),
    destroy=extend_schema(tags=['Bookings']),
)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        slot_id = request.data.get('slot')
        user_id = request.data.get('user')

        if not slot_id:
            return Response({"status": "slot_id is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({"status": "user_id is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot = Slot.objects.select_for_update().get(id=slot_id)
        except Slot.DoesNotExist:
            return Response({"status": "No Slot matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        if slot.is_booked:
            return Response({"status": "Slot already booked"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, pk=user_id)
        slot.is_booked = True
        slot.save()

        booking = Booking(user=user, slot=slot)

        zoom_meeting_url = self.create_zoom_meeting()
        if zoom_meeting_url:
            booking.meeting_url = zoom_meeting_url

        booking.save()

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    def create_zoom_meeting(self):
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            'authorization': f'Bearer {self.get_zoom_token()}',
            'content-type': 'application/json'
        }
        payload = {
            "topic": "Event Booking",
            "type": 2,
            "duration": 60,
            "settings": {
                "host_video": True,
                "participant_video": True
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f'data:{response.json()}')
        if response.status_code == 201:
            return response.json().get('join_url')
        return None
    
    
    
    def get_zoom_token(self):
        payload = {
            'grant_type':'account_credentials',
           'client_id':CLIENT_ID,
            'account_id':ACCOUNT_ID,
            'client_secret':CLIENT_SECRET
            
            }
        response=requests.post('https://zoom.us/oauth/token',data=payload)
        print(f"response:{response.json}")
        return response.json()['access_token']
       

   