from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


    
class ZoomIntegrationTests(APITestCase):
    meeting_id=None

    def setUp(self):
        # Setup code to run before each test (e.g., mock authentication)
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassuser', first_name='testuser')

        # Obtain token using LoginView
        login_url = reverse('booking:api-login')  # Replace with actual URL name or path to your LoginView
        login_data = {
            'email': 'testuser@test.com',
            'password': 'testpassuser'
        }
        response = self.client.post(login_url, login_data, format='json', verify=False)
        # print(f"Login response: {response.data}")

        if 'access' in response.data:
            self.token = response.data['access']
        else:
            self.token = None
            print("Login failed. Invalid credentials.")
            
    def test_create_meeting(self):
        global meeting_id
        if not self.token:
            self.fail("Token not obtained. Login failed.")

        url = 'http://127.0.0.1:8000/api/zoom/create-meeting/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        
        # Send POST request to create a Zoom meeting
        response = self.client.post(url, format='json', verify=False)

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Retrieve the meeting_id from the response data
        meeting_id = response.data.get('id')
        self.assertIsNotNone(meeting_id, "Meeting ID should be present in the response")

        

    def test_delete_meeting(self):
        global meeting_id
        if not self.token:
            self.fail("Token not obtained. Login failed.")

        # Call the create meeting method to get the meeting_id
        

        url = f'http://127.0.0.1:8000/api/zoom/meetings/{meeting_id}/'  # Adjust URL with meeting_id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        response = self.client.delete(url, format='json', verify=False)

        # Check if the response status code is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
