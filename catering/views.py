from django.shortcuts import render
from .models import CateringService
from booking.utils import is_service_booked


def catering_list(request):
    selected_date = request.GET.get('date')
    services = CateringService.objects.all()

    service_data = []

    for service in services:
        booked = False
        if selected_date:
            booked = is_service_booked(
                'catering',
                service.id,
                selected_date
            )

        service_data.append({
            'service': service,
            'is_booked': booked
        })

    return render(request, 'catering/catering_list.html', {
        'services': service_data,
        'selected_date': selected_date
    })
