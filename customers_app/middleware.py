
from datetime import timedelta

from django.utils import timezone

from .models import Customer, CustomerSession, CustomerActivity


class CustomerActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track only successful HTML page visits.
        if (
            request.method != "GET"
            or response.status_code != 200
            or not response.get("Content-Type", "").startswith("text/html")
        ):
            return response

        if not request.user.is_authenticated:
            return response

        # Exclude admin, static and media paths.
        if request.path.startswith(("/admin/", "/static/", "/media/")):
            return response

        customer = Customer.objects.filter(
            user_id=request.user.pk
        ).first()

        if not customer:
            return response

        session_id = request.session.get(
            "acz_monitoring_session_id"
        )

        if not session_id:
            return response

        customer_session = CustomerSession.objects.filter(
            pk=session_id,
            customer=customer,
            is_active=True,
        ).first()

        if not customer_session:
            return response

        now = timezone.now()

        # Update last activity at most once every 60 seconds.
        CustomerSession.objects.filter(
            pk=customer_session.pk,
            is_active=True,
            last_activity__lt=now - timedelta(seconds=60),
        ).update(last_activity=now)

        # Store page path only, never query parameters.
        ip_address = request.META.get("REMOTE_ADDR") or None

        CustomerActivity.objects.create(
            customer=customer,
            session=customer_session,
            event_type="PAGE_VISIT",
            page_path=request.path[:255],
            ip_address=ip_address,
            user_agent=request.META.get(
                "HTTP_USER_AGENT", ""
            )[:1000],
        )

        return response
