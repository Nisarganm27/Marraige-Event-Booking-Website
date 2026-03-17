from booking.models import Booking
from datetime import datetime

def is_service_booked(service_type, service_id, selected_date):
    if not selected_date:
        return False

    # convert string -> date
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

    return Booking.objects.filter(
        service_type=service_type,
        service_id=service_id,
        booking_date=date_obj
    ).exists()

def get_average_rating(service_type, service_id):
    avg = Review.objects.filter(
        service_type=service_type,
        service_id=service_id
    ).aggregate(Avg('rating'))['rating__avg']

    return round(avg, 1) if avg else None

