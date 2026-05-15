from django.contrib import admin
from django.urls import path, include
from customers_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers_app.urls')),

path('check-status/', views.check_status, name='check_status'),
]