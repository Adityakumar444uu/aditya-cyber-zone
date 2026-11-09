
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, Http404
from customers_app import views


def service_worker(request):
    """Serve the PWA service worker from the website root."""
    service_worker_path = (
        settings.BASE_DIR / "static" / "pwa" / "service-worker.js"
    )

    try:
        javascript = service_worker_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise Http404("Service worker file not found.")

    response = HttpResponse(
        javascript,
        content_type="application/javascript"
    )
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"

    return response


urlpatterns = [
    path(
        "service-worker.js",
        service_worker,
        name="service_worker"
    ),

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
