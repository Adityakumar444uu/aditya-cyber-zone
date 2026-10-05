from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customers_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers_app.urls')),

    path('check-status/', views.check_status, name='check_status'),
    path(
        "customer-forgot-password/",
        views.customer_forgot_password,
        name="customer_forgot_password"
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )