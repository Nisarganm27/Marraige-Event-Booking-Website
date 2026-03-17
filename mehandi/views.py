from django.shortcuts import render
from .models import MehandiService
from booking.utils import is_service_booked

def mehandi_list(request):
    selected_date = request.GET.get('date')
    services = MehandiService.objects.all()

    service_data = []

    if selected_date:
        for service in services:
            booked = is_service_booked(
                service_type='mehandi',
                service_id=service.id,
                booking_date=selected_date
            )
            service_data.append({
                'service': service,
                'booked': booked
            })
    else:
        for service in services:
            service_data.append({
                'service': service,
                'booked': False
            })

    return render(request, 'mehandi/mehandi_list.html', {
        'services': service_data,
        'selected_date': selected_date
    })
