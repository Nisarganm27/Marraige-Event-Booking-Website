from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from serviceprovider.models import Service
from .models import UserProfile
from booking.models import Booking


# ✅ HOME PAGE
def home(request):
    return render(request, "accounts/home.html")


# ✅ USER REGISTER
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("user_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("user_register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registered successfully! Please login.")
        return redirect("user_login")

    return render(request, "accounts/register.html")


# ✅ USER LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ✅ USER DASHBOARD
def user_dashboard(request):
    return render(request, "accounts/dashboard.html")

def register(request):
    return user_register(request)

def login_view(request):
    return user_login(request)

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    return user_dashboard(request)

def user_logout(request):
    logout(request)
    return redirect("home")

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Invalid admin credentials")
    return render(request, "accounts/admin_login.html")

def admin_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("admin_register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_register")
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()
        login(request, user)
        return redirect("admin_dashboard")
    return render(request, "accounts/admin_register.html")

def list_services(request, service_type):
    qs = Service.objects.filter(service_type=service_type, status='Approved')
    items = [{
        'id': s.id,
        'name': s.name,
        'location': s.location,
        'price': s.price,
        'provider_name': s.provider.username
    } for s in qs]
    return render(request, "accounts/category_list.html", {
        'service_type': service_type,
        'services': items
    })

def service_detail(request, service_id):
    s = get_object_or_404(Service, id=service_id)
    if s.status != 'Approved' and not (request.user.is_staff or request.user == s.provider):
        return HttpResponseForbidden()
    return render(request, "accounts/service_detail.html", { 'service': s, 'status': None })

def check_availability(request, service_id):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({ 'error': 'date is required' }, status=400)
    exists = Booking.objects.filter(service_id=service_id, booking_date=date).exists()
    return JsonResponse({ 'available': not exists })

@staff_member_required
def admin_dashboard(request):
    providers = User.objects.filter(Q(provided_services__isnull=False)).distinct().annotate(service_count=Count('provided_services'))
    # Ensure profiles exist to avoid template errors on u.userprofile.*
    for u in providers:
        UserProfile.objects.get_or_create(user=u)
    pending_services = Service.objects.filter(status='Pending')
    approved_services = Service.objects.filter(status='Approved')
    rejected_services = Service.objects.filter(status='Rejected')
    return render(request, "accounts/admin_dashboard.html", {
        'providers': providers,
        'pending_services': pending_services,
        'approved_services': approved_services,
        'rejected_services': rejected_services,
    })

@staff_member_required
def provider_list(request):
    providers = User.objects.filter(Q(provided_services__isnull=False)).distinct().annotate(service_count=Count('provided_services'))
    for u in providers:
        UserProfile.objects.get_or_create(user=u)
    return render(request, "accounts/admin_providers.html", { 'providers': providers })

@staff_member_required
def provider_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    services = Service.objects.filter(provider=user)
    return render(request, "accounts/admin_provider_detail.html", {
        'provider': user,
        'profile': profile,
        'services': services
    })

@staff_member_required
def approve_provider(request, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    user = get_object_or_404(User, id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.is_approved = True
    profile.save()
    return JsonResponse({ 'ok': True })

@staff_member_required
def reject_provider(request, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    user = get_object_or_404(User, id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.is_approved = False
    profile.save()
    return JsonResponse({ 'ok': True })

@staff_member_required
def approve_service(request, service_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    s = get_object_or_404(Service, id=service_id)
    s.status = 'Approved'
    s.save()
    return JsonResponse({ 'ok': True })

@staff_member_required
def reject_service(request, service_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    s = get_object_or_404(Service, id=service_id)
    s.status = 'Rejected'
    s.save()
    return JsonResponse({ 'ok': True })
