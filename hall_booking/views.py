from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from booking.models import Booking
from .models import MarriageHall

def hall_list(request):
    halls = MarriageHall.objects.all()
    date_str = request.GET.get('date')

    selected_date = None
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    hall_data = []

    for hall in halls:
        is_booked = False

        if selected_date:
            is_booked = Booking.objects.filter(
                service_type='hall',          # must match DB exactly
                service_id=hall.id,
                booking_date=selected_date,   # ✅ DATE object
                status='Booked'               # must match DB exactly
            ).exists()

        hall_data.append({
            'hall': hall,
            'is_booked': is_booked
        })

    return render(
        request,
        'hall_booking/halls.html',
        {
            'hall_data': hall_data,
            'selected_date': date_str  # keep string for template
        }
    )
@login_required
def add_hall(request):
    if request.method == 'POST':
        MarriageHall.objects.create(
            user=request.user,   # 🔥 MUST EXIST
            name=request.POST['name'],
            location=request.POST['location'],
            price=request.POST['price'],
            contact=request.POST['contact'],
        )
        return redirect('provider_dashboard')


    return render(request, 'hall_booking/add_hall.html')
