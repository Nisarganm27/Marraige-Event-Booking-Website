from django.db import models
from django.contrib.auth.models import User
from serviceprovider.models import Service

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    price = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.service.name} - {self.user.username}"
