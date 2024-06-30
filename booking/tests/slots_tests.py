from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from booking.models.booking_models import Slot
from booking.serializers import SlotSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model



class SlotViewSetTestCase(APITestCase):
    
    def setUp(self):
        # Setup code to run before each test (e.g., mock authentication)
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='testpassuser', first_name='testuser')

        # Obtain token using LoginView
        login_url = reverse('booking:api-login')  # Replace with actual URL name or path to your LoginView
        login_data = {
            'email': 'testuser@test.com',
            'password': 'testpassuser'
        }
        response = self.client.post(login_url, login_data, format='json')
        # print(f"Login response: {response.data}")

        if 'access' in response.data:
            self.token = response.data['access']
        else:
            self.token = None
            print("Login failed. Invalid credentials.")

    def test_list_slots(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        url = 'http://127.0.0.1:8000/api/slots/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        response = self.client.get(url,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Slot.objects.count())


    def test_create_slot(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        url = 'http://127.0.0.1:8000/api/slots/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        data={
            "start_time": "2024-06-30T15:44:09.009Z",
            "end_time": "2024-06-30T15:44:09.009Z",
            "is_booked": False
            }
        # Send POST request to create a Zoom meeting
        response = self.client.post(url, data,format='json',follow=True)
        print(f"response:{response.data['id']}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Slot.objects.filter(id=response.data['id']).exists())
        # Add more assertions as needed

    def test_update_slot(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        slots_obj=Slot.objects.create(start_time="2024-06-30T15:44:09.009Z", end_time="2024-06-30T15:44:09.009Z",is_booked=False)
        id = slots_obj.id
        # print(f"id:{id}")
        url = f'http://127.0.0.1:8000/api/slots/{id}/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        
        data={
            "start_time": "2024-06-30T15:44:09.009Z",
            "end_time": "2024-06-30T15:44:09.009Z",
            "is_booked": True
            }
        
        response = self.client.put(url, data,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Refresh the slots_obj from database to get the updated values
        slots_obj.refresh_from_db()
    
        # Perform assertions on the updated slot object
        self.assertTrue(slots_obj.is_booked)  # Check if the slot is updated correctly
       


    def test_delete_slot(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        slots_obj=Slot.objects.create(start_time="2024-06-30T15:44:09.009Z", end_time="2024-06-30T15:44:09.009Z",is_booked=False)
        id = slots_obj.id
        # print(f"id:{id}")
        url = f'http://127.0.0.1:8000/api/slots/{id}/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        response = self.client.delete(url,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Slot.objects.filter(id=slots_obj.id).exists())

