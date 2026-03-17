from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("user-login/", views.user_login, name="user_login"),
    path("user-register/", views.user_register, name="user_register"),
    path("logout/", views.user_logout, name="user_logout"),


    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-register/", views.admin_register, name="admin_register"),
    path("admin/providers/", views.provider_list, name="admin_providers"),
    path("admin/providers/<int:user_id>/", views.provider_detail, name="admin_provider_detail"),
    path("admin/providers/<int:user_id>/approve/", views.approve_provider, name="approve_provider"),
    path("admin/providers/<int:user_id>/reject/", views.reject_provider, name="reject_provider"),
    path("admin/services/<int:service_id>/approve/", views.approve_service, name="approve_service"),
    path("admin/services/<int:service_id>/reject/", views.reject_service, name="reject_service"),
    path("services/<str:service_type>/", views.list_services, name="list_services"),
    path("service/<int:service_id>/", views.service_detail, name="service_detail"),
    path("service/<int:service_id>/availability/", views.check_availability, name="check_availability"),
]
