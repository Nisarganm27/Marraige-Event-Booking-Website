from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from .utils import is_service_booked
from booking.models import  Booking
from serviceprovider.models import Service
from django.http import JsonResponse

@login_required
def book_service(request, service_type, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    date = request.POST.get("date") or request.GET.get("date")

    if not date:
        return redirect("service_detail", service_id=service_id)

    # Prevent double booking if already exists
    if Booking.objects.filter(service=service, booking_date=date).exists():
        return redirect("service_detail", service_id=service_id)

    Booking.objects.create(
        user=request.user,
        service=service,
        booking_date=date,
        price=service.price,
        status='Pending'
    )

    return redirect("my_bookings")


@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/user_bookings.html', {'bookings': bookings})

@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status != 'Accepted':
        return render(request, 'booking/payment.html', {'booking': booking, 'error': 'Payment is available only after provider accepts the booking.'})

    if request.method == 'POST':
        booking.status = 'Paid'
        booking.save()
        return redirect('payment_success')

    return render(request, 'booking/payment.html', {'booking': booking})


@login_required
def payment_success(request):
    return render(request, 'booking/payment_success.html')


@login_required
def add_review(request, service_type, service_id):
    booking_exists = Booking.objects.filter(
        user=request.user,
        service_type=service_type,
        service_id=service_id,
        status='Paid'
    ).exists()

    if not booking_exists:
        return HttpResponse("You can only rate after booking.")

    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            service_type=service_type,
            service_id=service_id,
            rating=request.POST['rating'],
            comment=request.POST.get('comment', '')
        )
        return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'booking/add_review.html')
@login_required
def create_booking(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        Booking.objects.create(
    user=request.user,
    service=service,
    booking_date=date,
    service_type=service.service_type,
    price=service.price,
    status='Pending'
)

        return redirect('my_bookings')

    return render(request, 'booking/create_booking.html', {'service': service})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('service', 'service__provider')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})
def check_availability(request, service_id):
    date = request.GET.get("date")

    if not date:
        return JsonResponse({"available": False})

    exists = Booking.objects.filter(
    service_id=service_id,
    booking_date=date
).exists()


    return JsonResponse({
        "available": not exists
    })
