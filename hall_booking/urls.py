from django.urls import path
from .views import hall_list, add_hall   # 👈 add this

urlpatterns = [
    path('', hall_list, name='hall_list'),
    path('add/', add_hall, name='add_hall'),
]
