from django.urls import path
from . import views

urlpatterns = [
    path('', views.photographer_list, name='photographer_list'),
]
