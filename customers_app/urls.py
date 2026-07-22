from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),

    path('customer-register/', views.customer_register, name='customer_register'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),

    path('pay-now/<int:app_id>/', views.create_payment, name='create_payment'),
    path('payment-success/<int:app_id>/', views.payment_success, name='payment_success'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('receipt/<int:app_id>/', views.receipt, name='receipt'),

    path('check-status/', views.check_status, name='check_status'),

    path('customers/', views.customer_list, name='customer_list'),
    path('applications/', views.all_applications, name='all_applications'),
    path('add-application/', views.add_application, name='add_application'),
    path('update-status/<int:app_id>/', views.update_status, name='update_status'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    path('raise-grievance/', views.raise_grievance, name='raise_grievance'),
    path('grievance-status/', views.grievance_status, name='grievance_status'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),

    path('bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
    path("ai-chat/", views.ai_chat, name="ai_chat"),
path(
        "kriparohii/verify/",
        views.kriparohii_verify,
        name="kriparohii_verify"
    ),
path(
    "kriparohii/status/",
    views.kriparohii_status,
    name="kriparohii_status"
),
path(
    "kriparohii/chat/",
    views.kriparohii_chat,
    name="kriparohii_chat"
),
path(
    "kriparohii/grievance/",
    views.kriparohii_grievance
),
]