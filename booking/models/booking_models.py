# bookings/models.py

from django.db import models
from .user_models import CustomUser

class Slot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    meeting_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} booked {self.slot}"
