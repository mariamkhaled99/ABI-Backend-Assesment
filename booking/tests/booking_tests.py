from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from booking.models.booking_models import Booking, Slot
from booking.models.user_models import CustomUser


class BookingViewSetTestCase(APITestCase):
    
    def setUp(self):
        # Setup code to run before each test (e.g., mock authentication)
        self.user = CustomUser.objects.create_user(email='testuser@test.com', password='testpassuser', first_name='testuser')
        self.slot = Slot.objects.create(start_time="2024-06-30T15:44:09.009Z", end_time="2024-06-30T15:44:09.009Z", is_booked=False)
        
        # Obtain token using LoginView
        login_url = reverse('booking:api-login')  # Replace with actual URL name or path to your LoginView
        login_data = {
            'email': 'testuser@test.com',
            'password': 'testpassuser'
        }
        response = self.client.post(login_url, login_data, format='json')

        if 'access' in response.data:
            self.token = response.data['access']
        else:
            self.token = None
            self.fail("Token not obtained. Login failed.")

    def test_list_booking(self):
        if not self.token:
            self.fail("Token not obtained. Login failed.")
        
        url = 'http://127.0.0.1:8000/api/bookings/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Booking.objects.count())

    def test_delete_booking(self):
        if not self.token:
            self.fail("Token not obtained. Login failed.")
        
        booking_obj = Booking.objects.create(meeting_url="", user=self.user, slot=self.slot)
        booking_id = booking_obj.id
        url = f'http://127.0.0.1:8000/api/bookings/{booking_id}/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        
        response = self.client.delete(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())





    def test_create_booking(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        url = 'http://127.0.0.1:8000/api/bookings/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        
        data={
            "meeting_url": "",
            "user": self.user.id,
            "slot": self.slot.id
            }
        # Send POST request to create a Zoom meeting
        response = self.client.post(url, data,format='json',follow=True, verify=False)
        # print(f"response:{response.data['id']}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Slot.objects.filter(id=response.data['id']).exists())
       

    def test_update_slot(self):
        if not self.token:
                self.fail("Token not obtained. Login failed.")
        
        
        booking_obj = Booking.objects.create(meeting_url="", user=self.user, slot=self.slot)
        id = booking_obj.id
        url = f'http://127.0.0.1:8000/api/bookings/{id}/'  # Adjust URL as per your actual endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate using token
        
        data={
            "meeting_url": "",
            "user": self.user.id,
            "slot": self.slot.id
            }
    
        response = self.client.put(url, data,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the slots_obj from database to get the updated values
        booking_obj.refresh_from_db()
    
        
       