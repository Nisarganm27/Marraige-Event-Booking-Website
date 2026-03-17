from django.urls import path
from . import views

urlpatterns = [
    path('', views.catering_list, name='catering_list'),
]
