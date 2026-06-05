from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),

    path('customer-register/', views.customer_register, name='customer_register'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),

    path('check-status/', views.check_status, name='check_status'),

    path('customers/', views.customer_list, name='customer_list'),
    path('applications/', views.all_applications, name='all_applications'),
    path('add-application/', views.add_application, name='add_application'),
    path('update-status/<int:app_id>/', views.update_status, name='update_status'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    path('raise-grievance/', views.raise_grievance, name='raise_grievance'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),
]