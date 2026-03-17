from django.shortcuts import render
from .models import Photographer
from booking.utils import is_service_booked

def photographer_list(request):
    selected_date = request.GET.get('date')
    photographers = Photographer.objects.all()

    data = []
    for p in photographers:
        booked = False
        if selected_date:
            booked = is_service_booked('photography', p.id, selected_date)

        data.append({
            'service': p,
            'is_booked': booked
        })

    return render(request, 'photography/photographer_list.html', {
        'photographers': data,
        'selected_date': selected_date
    })
