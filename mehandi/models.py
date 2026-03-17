from django.db import models

class MehandiService(models.Model):
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name
