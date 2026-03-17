from django.urls import path
from . import views

urlpatterns = [
    path(
    'book/new/<str:service_type>/<int:service_id>/',
    views.book_service,
    name='book_service'
),
path("service/<int:service_id>/availability/", views.check_availability, name="check_availability"),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
