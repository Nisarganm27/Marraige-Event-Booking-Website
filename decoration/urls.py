from django.urls import path
from . import views

urlpatterns = [
    path('', views.decoration_list, name='decoration_list'),
]
