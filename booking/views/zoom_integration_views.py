from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

import requests
from django.conf import settings
import jwt
import time




# Zoom Configuration
ACCOUNT_ID = settings.ACCOUNT_ID
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

@extend_schema_view(
    create_meeting=extend_schema(tags=['Zoom Integration'], summary="Create a new Zoom meeting."),
    list_meetings=extend_schema(tags=['Zoom Integration'], summary="Retrieve all Zoom meetings for the logged-in user."),
    delete_meeting=extend_schema(tags=['Zoom Integration'], summary="Delete a Zoom meeting by ID."),
)
class ZoomIntegrationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Create a new Zoom meeting",
        request=None,
        responses={201: OpenApiResponse(description="Zoom meeting created successfully")}
    )
    @action(detail=False, methods=['post'], url_path='create-meeting')
    def create_meeting(self, request):
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            'authorization': f'Bearer {self.get_zoom_token()}',
            'content-type': 'application/json'
        }
        payload = {
            "topic": "New Meeting",
            "type": 2,
            "duration": 60,
            "settings": {
                "host_video": "true",
                "participant_video": "true"
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return Response(response.json(), status=status.HTTP_201_CREATED)
        return Response(response.json(), status=response.status_code)

    @extend_schema(
        summary="Retrieve all Zoom meetings",
        request=None,
        responses={200: OpenApiResponse(description="List of Zoom meetings")}
    )
    @action(detail=False, methods=['get'], url_path='meetings')
    def list_meetings(self, request):
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            'authorization': f'Bearer {self.get_zoom_token()}',
            'content-type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)

    @extend_schema(
        summary="Delete a Zoom meeting by ID",
        request=None,
        responses={204: OpenApiResponse(description="Zoom meeting deleted successfully")}
    )
    @action( detail=False,methods=['delete'], url_path='meetings/(?P<id>[^/.]+)')
    def delete_meeting(self, request, id=None):
        url = f"https://api.zoom.us/v2/meetings/{id}"
        headers = {
            'Authorization': f'Bearer {self.get_zoom_token()}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 204:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(response.json(), status=response.status_code)

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
    
       
   