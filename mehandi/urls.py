from django.urls import path
from .views import mehandi_list

urlpatterns = [
    path('', mehandi_list, name='mehandi_list'),
]
