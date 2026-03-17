from django.db import models
from django.contrib.auth.models import User

class MarriageHall(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='halls'
)
 # provider
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name
