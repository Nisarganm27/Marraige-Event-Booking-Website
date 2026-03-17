from django.db import models

class CateringService(models.Model):
    MENU_CHOICES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
        ('Both', 'Both'),
    ]

    name = models.CharField(max_length=100)
    menu_type = models.CharField(max_length=10, choices=MENU_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=15)   # ✅ contact number

    def __str__(self):
        return self.name
