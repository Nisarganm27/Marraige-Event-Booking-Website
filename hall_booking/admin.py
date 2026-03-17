from django.contrib import admin
from .models import MarriageHall

@admin.register(MarriageHall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact', 'price')
