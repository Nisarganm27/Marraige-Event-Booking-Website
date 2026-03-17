from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    # Home Page
    path('', account_views.home, name='home'),

    # User Authentication
    path('register/', account_views.register, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', account_views.dashboard, name='dashboard'),

    # Services (later)
    path('provider/', include('serviceprovider.urls')),
    path('book/', include('booking.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin-dashboard/', account_views.admin_dashboard, name='admin_dashboard_root'),
    path("booking/", include("booking.urls")),

]
