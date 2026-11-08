import hashlib
import hmac
import json
import uuid
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User

from .google_sheet import sync_application_to_sheet

from .models import (
    Application,
    ApplicationStatusHistory,
    Customer,
    Grievance,
    GrievanceHistory,
    Notice,
    PaymentHistory,
    PayUTransaction,
    UpiPaymentSubmission,
)



# -----------------------------------------------------------------------------
# ADMIN / APPLICATION MANAGEMENT
# -----------------------------------------------------------------------------

@staff_member_required
def customer_list(request):
    return render(request, "customer_list.html", {
        "customers": Customer.objects.all().order_by("-id"),
        "recent_applications": Application.objects.all().order_by("-id")[:5],
        "recent_grievances": Grievance.objects.all().order_by("-id")[:5],
        "total_customers": Customer.objects.count(),
        "total_applications": Application.objects.count(),
        "pending_count": Application.objects.filter(status="Pending").count(),
        "submitted_count": Application.objects.filter(status="Submitted").count(),
        "in_process_count": Application.objects.filter(status="In Process").count(),
        "approved_count": Application.objects.filter(status="Approved").count(),
        "rejected_count": Application.objects.filter(status="Rejected").count(),
        "delivered_count": Application.objects.filter(status="Delivered").count(),
        "pending_applications": Application.objects.filter(status="Pending").count(),
        "delivered_applications": Application.objects.filter(status="Delivered").count(),
        "total_grievances": Grievance.objects.count(),
        "open_grievances": Grievance.objects.exclude(status__in=["Resolved", "Closed"]).count(),
        "resolved_grievances": Grievance.objects.filter(status="Resolved").count(),
    })


@staff_member_required
def all_applications(request):
    selected_status = request.GET.get("status", "").strip()
    applications = Application.objects.select_related("customer", "part", "sub_part").all()
    if selected_status:
        valid_statuses = {value for value, _ in Application.STATUS_CHOICES}
        if selected_status in valid_statuses:
            applications = applications.filter(status=selected_status)
    return render(request, "all_applications.html", {
        "applications": applications.order_by("-application_date", "-id"),
        "selected_status": selected_status,
    })


@staff_member_required
def add_application(request):
    customers = Customer.objects.all().order_by("name")
    if request.method == "POST":
        customer = get_object_or_404(Customer, id=request.POST.get("customer"))
        application = Application.objects.create(
            customer=customer,
            application_name=(request.POST.get("application_name") or "").strip(),
            application_no=(request.POST.get("application_no") or "").strip(),
            application_date=timezone.localdate(),
            status=request.POST.get("status") or "Pending",
        )
        sync_application_to_sheet(application)
        messages.success(request, "Application added successfully.")
        return redirect("all_applications")
    return render(request, "add_application.html", {"customers": customers})


@staff_member_required
def update_status(request, app_id):
    if request.method != "POST":
        return redirect("all_applications")

    application = get_object_or_404(Application, id=app_id)
    new_status = request.POST.get("status")
    remark = (request.POST.get("remark") or request.POST.get("remarks") or "").strip()
    valid_statuses = {value for value, _ in Application.STATUS_CHOICES}
    if new_status not in valid_statuses:
        messages.error(request, "Invalid application status.")
        return redirect("all_applications")

    application.status = new_status
    application.remarks = remark
    application.delivery_date = timezone.now() if new_status == "Delivered" else None
    application.save()
    ApplicationStatusHistory.objects.create(application=application, status=new_status, remark=remark)
    sync_application_to_sheet(application, remark)
    messages.success(request, "Application status updated.")
    return redirect("all_applications")


@staff_member_required
def bulk_update_status(request):
    if request.method != "POST":
        return redirect("all_applications")

    selected_ids = request.POST.getlist("selected_applications")
    new_status = request.POST.get("bulk_status")
    remark = (request.POST.get("bulk_remark") or "").strip()
    valid_statuses = {value for value, _ in Application.STATUS_CHOICES}
    if selected_ids and new_status in valid_statuses:
        for application in Application.objects.filter(id__in=selected_ids).select_related("customer"):
            application.status = new_status
            application.remarks = remark
            application.delivery_date = timezone.now() if new_status == "Delivered" else None
            application.save()
            ApplicationStatusHistory.objects.create(application=application, status=new_status, remark=remark)
            sync_application_to_sheet(application, remark)
        messages.success(request, "Selected application statuses updated.")
    else:
        messages.error(request, "Please select applications and a valid status.")
    return redirect("all_applications")


@staff_member_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    applications = Application.objects.filter(customer=customer).order_by("-application_date", "-id")
    return render(request, "customer_detail.html", {"customer": customer, "applications": applications})


# -----------------------------------------------------------------------------
# PUBLIC APPLICATION STATUS
# -----------------------------------------------------------------------------

def check_status(request):
    application = None
    error = None
    application_no = (request.GET.get("application_no") or "").strip()
    if application_no:
        application = Application.objects.filter(application_no=application_no).select_related("customer").first()
        if application is None:
            error = "Application Not Found"
    return render(request, "check_status.html", {"application": application, "error": error})


@require_GET
def live_application_counts(request):
    statuses = ["Pending", "Submitted", "In Process", "Approved", "Rejected", "Delivered"]
    counts = {status: Application.objects.filter(status=status).count() for status in statuses}
    return JsonResponse({"counts": counts, "total": sum(counts.values())})


# -----------------------------------------------------------------------------
# CUSTOMER REGISTRATION / LOGIN
# -----------------------------------------------------------------------------

def customer_register(request):
    message = ""
    customer = None

    if request.method == "POST" and "verify" in request.POST:
        aadhaar_no = (request.POST.get("aadhaar_no") or "").strip()
        customer = Customer.objects.filter(aadhaar_no=aadhaar_no).first()
        if customer is None:
            message = "Aadhaar not found. Please contact Admin."
        elif customer.user_id:
            message = "Account already created. Please login."
        else:
            return render(request, "customer_register.html", {"customer": customer, "message": ""})

    elif request.method == "POST" and "register" in request.POST:
        aadhaar_no = (request.POST.get("aadhaar_no") or "").strip()
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""
        customer = Customer.objects.filter(aadhaar_no=aadhaar_no).first()
        if customer is None:
            message = "Customer not found."
        elif customer.user_id:
            message = "Account already exists. Please login."
        elif len(password) < 6:
            message = "Password must be at least 6 characters."
        elif password != confirm_password:
            message = "Password does not match."
        else:
            with transaction.atomic():
                customer = Customer.objects.select_for_update().get(pk=customer.pk)
                if customer.user_id:
                    message = "Account already exists. Please login."
                else:
                    user = User.objects.create_user(
                        username=customer.aadhaar_no,
                        password=password,
                        first_name=customer.name,
                    )
                    customer.user = user
                    customer.is_registered = True
                    customer.save(update_fields=["user", "is_registered"])
                    return redirect("/customer-login/?registered=1")

    return render(request, "customer_register.html", {"message": message, "customer": customer})


def customer_login(request):
    error = None
    if request.method == "POST":
        aadhaar_no = (request.POST.get("aadhaar_no") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=aadhaar_no, password=password)
        if user is not None and user.is_active:
            customer = Customer.objects.filter(user=user).first()
            if customer:
                login(request, user)
                return redirect("customer_dashboard")
        error = "Invalid Aadhaar Number or Password."

    return render(request, "customer_login.html", {
        "error": error,
        "registered": request.GET.get("registered") == "1",
    })


@login_required
def customer_dashboard(request):
    customer = Customer.objects.filter(user=request.user).first()
    if customer is None:
        logout(request)
        return redirect("/customer-login/")

    applications = (
        Application.objects.filter(customer=customer)
        .prefetch_related("upi_payment_submissions", "payment_history")
        .order_by("-id")
    )
    totals = applications.aggregate(
        total_amount=Sum("amount"),
        total_paid=Sum("paid_amount"),
        total_due=Sum("due_amount"),
    )
    payment_history = (
        PaymentHistory.objects.filter(application__customer=customer)
        .select_related("application")
        .order_by("-created_at")
    )
    return render(request, "customer_dashboard.html", {
        "customer": customer,
        "applications": applications,
        "total_amount": totals["total_amount"] or Decimal("0.00"),
        "total_paid": totals["total_paid"] or Decimal("0.00"),
        "total_due": totals["total_due"] or Decimal("0.00"),
        "payment_history": payment_history,
    })


@login_required
def customer_logout(request):
    logout(request)
    return redirect("/customer-login/?success=1")


# -----------------------------------------------------------------------------
# PAYU PAYMENT INTEGRATION
# -----------------------------------------------------------------------------



def _payu_reverse_hash(post_data):
    """Build PayU's reverse hash from PayU response fields."""
    salt = getattr(settings, "PAYU_MERCHANT_SALT", "")

    fields = [
        salt,
        post_data.get("status", ""),
        "", "", "", "", "", "", "", "", "",
        post_data.get("udf5", ""),
        post_data.get("udf4", ""),
        post_data.get("udf3", ""),
        post_data.get("udf2", ""),
        post_data.get("udf1", ""),
        post_data.get("email", ""),
        post_data.get("firstname", ""),
        post_data.get("productinfo", ""),
        post_data.get("amount", ""),
        post_data.get("txnid", ""),
        post_data.get("key", ""),
    ]

    hash_string = "|".join(str(value) for value in fields)

    additional_charges = (
        post_data.get("additionalCharges")
        or post_data.get("additional_charges")
    )

    if additional_charges:
        hash_string = f"{additional_charges}|{hash_string}"

    return hashlib.sha512(
        hash_string.encode("utf-8")
    ).hexdigest().lower()


def _payu_hash_matches(post_data):
    received_hash = (post_data.get("hash") or "").lower().strip()
    calculated_hash = _payu_reverse_hash(post_data)

    return bool(
        received_hash
        and hmac.compare_digest(received_hash, calculated_hash)
    )


def _valid_payu_response(post_data, expected_txnid, expected_amount):
    merchant_key = getattr(settings, "PAYU_MERCHANT_KEY", "")
    merchant_salt = getattr(settings, "PAYU_MERCHANT_SALT", "")

    if not merchant_key or not merchant_salt:
        return False, "PayU credentials are not configured."

    if post_data.get("key") != merchant_key:
        return False, "Invalid payment merchant key."

    if post_data.get("status", "").lower() != "success":
        return False, "Payment failed or cancelled."

    if not expected_txnid or post_data.get("txnid") != expected_txnid:
        return False, "Transaction ID mismatch."

    try:
        received_amount = Decimal(
            str(post_data.get("amount", "0"))
        ).quantize(Decimal("0.01"))

        required_amount = Decimal(
            str(expected_amount)
        ).quantize(Decimal("0.01"))

    except (InvalidOperation, TypeError, ValueError):
        return False, "Invalid payment amount."

    if received_amount != required_amount:
        return False, "Payment amount mismatch."

    if not _payu_hash_matches(post_data):
        return False, "Payment response hash could not be verified."

    return True, "Verified"


@login_required
def create_payment(request, app_id):
    application = get_object_or_404(
        Application.objects.select_related("customer"),
        id=app_id,
        customer__user=request.user,
    )

    merchant_key = getattr(settings, "PAYU_MERCHANT_KEY", "")
    merchant_salt = getattr(settings, "PAYU_MERCHANT_SALT", "")
    payu_url = getattr(settings, "PAYU_BASE_URL", "")

    if not merchant_key or not merchant_salt or not payu_url:
        messages.error(
            request,
            "Online payment abhi configure nahi hai. Please contact Aditya Cyber Zone."
        )
        return redirect("customer_dashboard")

    # Lock application so simultaneous requests reuse the same pending transaction.
    with transaction.atomic():
        locked_application = (
            Application.objects.select_for_update()
            .select_related("customer")
            .get(pk=application.pk)
        )

        amount = Decimal(
            locked_application.due_amount
        ).quantize(Decimal("0.01"))

        if amount <= 0:
            messages.info(
                request,
                "Is application ka koi due amount nahi hai."
            )
            return redirect("receipt", app_id=locked_application.id)

        pending_transaction = (
            PayUTransaction.objects.select_for_update()
            .filter(
                application=locked_application,
                status="Pending",
            )
            .order_by("-created_at")
            .first()
        )

        # Reuse an existing pending transaction for the same due amount.
        if pending_transaction and pending_transaction.amount == amount:
            payu_transaction = pending_transaction

        else:
            # An old pending transaction with a different amount is no longer usable.
            if pending_transaction:
                pending_transaction.status = "Failed"
                pending_transaction.save(update_fields=["status", "updated_at"])

            txnid = f"ACZ{locked_application.id}{uuid.uuid4().hex[:18]}"

            payu_transaction = PayUTransaction.objects.create(
                application=locked_application,
                txnid=txnid,
                amount=amount,
                status="Pending",
            )

    amount_text = f"{payu_transaction.amount:.2f}"
    txnid = payu_transaction.txnid

    firstname = locked_application.customer.name or "Customer"
    email = getattr(
        settings,
        "PAYU_CUSTOMER_EMAIL",
        "support@adityacyberzone.com",
    )
    phone = locked_application.customer.contact_no or ""
    productinfo = (
        locked_application.application_name
        or f"ACZ Application {locked_application.id}"
    )

    request_hash_string = (
        f"{merchant_key}|{txnid}|{amount_text}|{productinfo}|"
        f"{firstname}|{email}|||||||||||{merchant_salt}"
    )

    payu_hash = hashlib.sha512(
        request_hash_string.encode("utf-8")
    ).hexdigest().lower()

    callback_url = request.build_absolute_uri(
        f"/payment-success/{locked_application.id}/"
    )

    payu_data = {
        "key": merchant_key,
        "txnid": txnid,
        "amount": amount_text,
        "productinfo": productinfo,
        "firstname": firstname,
        "email": email,
        "phone": phone,
        "surl": callback_url,
        "furl": callback_url,
        "hash": payu_hash,
        "service_provider": "payu_paisa",
    }

    return render(
        request,
        "pay_now.html",
        {
            "application": locked_application,
            "payu_data": payu_data,
            "payu_url": payu_url,
        },
    )


@csrf_exempt
def payment_success(request, app_id):
    """Verify PayU callback and record a payment exactly once."""

    if request.method != "POST":
        return HttpResponseBadRequest(
            "Invalid payment callback method."
        )

    post_data = request.POST
    txnid = (post_data.get("txnid") or "").strip()
    mihpayid = (post_data.get("mihpayid") or "").strip()

    if not txnid:
        return render(
            request,
            "payment_failed.html",
            {"message": "Payment transaction ID is missing."},
        )

    with transaction.atomic():

        try:
            payu_transaction = (
                PayUTransaction.objects.select_for_update()
                .get(
                    application_id=app_id,
                    txnid=txnid,
                )
            )
        except PayUTransaction.DoesNotExist:
            return render(
                request,
                "payment_failed.html",
                {"message": "Payment transaction record not found."},
            )

        locked_application = (
            Application.objects.select_for_update()
            .select_related("customer")
            .get(pk=payu_transaction.application_id)
        )

        # Idempotency: repeated successful callbacks cannot credit twice.
        if payu_transaction.status == "Success":
            return render(
                request,
                "payment_success.html",
                {"application": locked_application},
            )

        if payu_transaction.status != "Pending":
            return render(
                request,
                "payment_failed.html",
                {"message": "This payment transaction is no longer pending."},
            )

        # Verify failure callbacks before changing transaction status.
        if post_data.get("status", "").lower() != "success":
            merchant_key = getattr(settings, "PAYU_MERCHANT_KEY", "")

            if (
                post_data.get("key") == merchant_key
                and _payu_hash_matches(post_data)
            ):
                payu_transaction.status = "Failed"
                payu_transaction.mihpayid = mihpayid
                payu_transaction.save(
                    update_fields=["status", "mihpayid", "updated_at"]
                )

            return render(
                request,
                "payment_failed.html",
                {"message": "Payment failed or cancelled."},
            )

        is_valid, validation_message = _valid_payu_response(
            post_data,
            expected_txnid=payu_transaction.txnid,
            expected_amount=payu_transaction.amount,
        )

        if not is_valid:
            return render(
                request,
                "payment_failed.html",
                {"message": validation_message},
            )

        try:
            payment_amount = Decimal(
                str(post_data.get("amount", "0"))
            ).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError, ValueError):
            return render(
                request,
                "payment_failed.html",
                {"message": "Invalid payment amount."},
            )

        current_due = Decimal(
            locked_application.due_amount
        ).quantize(Decimal("0.01"))

        if payment_amount <= 0 or payment_amount > current_due:
            return render(
                request,
                "payment_failed.html",
                {
                    "message": (
                        "Payment amount does not match "
                        "the outstanding balance."
                    )
                },
            )

        # Credit the application only after successful verification.
        locked_application.paid_amount = (
            Decimal(locked_application.paid_amount) + payment_amount
        )
        locked_application.payment_mode = "Online"
        locked_application.razorpay_payment_id = mihpayid or txnid
        locked_application.payment_reference_no = txnid
        locked_application.save()

        PaymentHistory.objects.create(
            application=locked_application,
            amount=payment_amount,
            payment_mode="Online",
            payment_status="Paid",
            payment_reference_no=txnid,
            receipt_no=locked_application.receipt_no or "",
        )

        payu_transaction.status = "Success"
        payu_transaction.mihpayid = mihpayid
        payu_transaction.save(
            update_fields=["status", "mihpayid", "updated_at"]
        )

    return render(
        request,
        "payment_success.html",
        {"application": locked_application},
    )



# -----------------------------------------------------------------------------
# PAYMENT HISTORY / RECEIPTS
# -----------------------------------------------------------------------------

@login_required
def payment_history(request):
    customer = Customer.objects.filter(user=request.user).first()
    history = PaymentHistory.objects.none()
    if customer:
        history = PaymentHistory.objects.filter(application__customer=customer).select_related("application").order_by("-created_at")
    return render(request, "payment_history.html", {"history": history})


@never_cache
def payment_history_search(request):
    customer = None
    applications = []
    history = []
    error = None
    searched = False
    search_type = "mobile_no"

    if request.method == "POST":
        searched = True
        search_type = (request.POST.get("search_type") or "mobile_no").strip()
        search_value = (request.POST.get("search_value") or "").strip()
        verify_aadhaar = (request.POST.get("verify_aadhaar") or "").strip()
        verify_mobile = (request.POST.get("verify_mobile") or "").strip()
        valid_types = {"aadhaar_no", "mobile_no", "application_no"}

        if search_type not in valid_types:
            error = "Please select a valid search option."
        elif not search_value:
            error = "Please enter the value to search."
        elif search_type == "aadhaar_no":
            if not verify_mobile:
                error = "Please enter your registered mobile number."
            else:
                customer = Customer.objects.filter(aadhaar_no=search_value, contact_no=verify_mobile).first()
        elif search_type == "mobile_no":
            if not verify_aadhaar:
                error = "Please enter your Aadhaar number."
            else:
                customer = Customer.objects.filter(contact_no=search_value, aadhaar_no=verify_aadhaar).first()
        else:
            if not verify_aadhaar or not verify_mobile:
                error = "Please enter both Aadhaar and registered mobile number."
            else:
                application = Application.objects.filter(
                    application_no=search_value,
                    customer__aadhaar_no=verify_aadhaar,
                    customer__contact_no=verify_mobile,
                ).select_related("customer").first()
                if application:
                    customer = application.customer
                    applications = [application]

        if not error and customer is None:
            error = "Details could not be verified. Please check and try again."
        if not error and customer:
            if search_type != "application_no":
                applications = list(Application.objects.filter(customer=customer).order_by("-application_date", "-id"))
            history = PaymentHistory.objects.filter(application__in=applications).select_related("application").order_by("-created_at")
        if error:
            customer, applications, history = None, [], []

    response = render(request, "payment_history_search.html", {
        "customer": customer,
        "applications": applications,
        "history": history,
        "error": error,
        "searched": searched,
        "search_type": search_type,
    })
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    return response


@login_required
def receipt(request, app_id):
    application = get_object_or_404(Application, id=app_id, customer__user=request.user)
    return render(request, "receipt.html", {"application": application})


@login_required
def consolidated_receipt(request):
    customer = Customer.objects.filter(user=request.user).first()
    if customer is None:
        applications = Application.objects.none()
        total_paid = Decimal("0.00")
        total_due = Decimal("0.00")
    else:
        applications = Application.objects.filter(customer=customer).order_by("-application_date", "-id")
        totals = applications.aggregate(total_paid=Sum("paid_amount"), total_due=Sum("due_amount"))
        total_paid = totals["total_paid"] or Decimal("0.00")
        total_due = totals["total_due"] or Decimal("0.00")

    response = render(request, "consolidated_receipt.html", {
        "applications": applications,
        "customer": customer,
        "total_paid": total_paid,
        "total_due": total_due,
        "public_view": False,
    })
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    return response


# -----------------------------------------------------------------------------
# GRIEVANCE REGISTRATION / TRACKING
# -----------------------------------------------------------------------------

def raise_grievance(request):
    customer = None
    applications = []
    ticket_no = None
    message = None
    error = None

    if request.method == "POST" and "verify_aadhaar" in request.POST:
        aadhaar_no = (request.POST.get("aadhaar_no") or "").strip()
        if not aadhaar_no:
            error = "Please enter your Aadhaar number."
        else:
            customer = Customer.objects.filter(aadhaar_no=aadhaar_no).first()
            if customer is None:
                error = "Aadhaar number not found. Please contact Aditya Cyber Zone."
            else:
                applications = Application.objects.filter(customer=customer).select_related("part", "sub_part").order_by("-application_date", "-id")
                request.session["grievance_customer_id"] = customer.id
                request.session["grievance_aadhaar_verified"] = True
                message = "Aadhaar verified successfully."

    elif request.method == "POST" and "submit_grievance" in request.POST:
        customer_id = request.session.get("grievance_customer_id")
        verified = request.session.get("grievance_aadhaar_verified", False)
        if not verified or not customer_id:
            error = "Please verify your Aadhaar first."
        else:
            customer = Customer.objects.filter(id=customer_id).first()
            if customer is None:
                error = "Customer verification expired. Please verify Aadhaar again."
                request.session.pop("grievance_customer_id", None)
                request.session.pop("grievance_aadhaar_verified", None)
            else:
                applications = Application.objects.filter(customer=customer).select_related("part", "sub_part").order_by("-application_date", "-id")
                application_id = request.POST.get("application_id")
                if not application_id:
                    error = "Please select an application."
                else:
                    application = Application.objects.filter(id=application_id, customer=customer).first()
                    if application is None:
                        error = "Selected application is invalid. Please select one of your applications."
                    else:
                        subject = (request.POST.get("subject") or "General Grievance").strip()[:200]
                        category = (request.POST.get("category") or "").strip()
                        priority = (request.POST.get("priority") or "Normal").strip()
                        description = (request.POST.get("description") or "").strip()
                        attachment = request.FILES.get("attachment")
                        valid_priorities = {value for value, _ in Grievance.PRIORITY_CHOICES}
                        if not category:
                            error = "Please select a grievance category."
                        elif not description:
                            error = "Please enter your grievance description."
                        elif priority not in valid_priorities:
                            error = "Please select a valid priority."
                        else:
                            grievance = Grievance.objects.create(
                                customer=customer,
                                application=application,
                                name=customer.name,
                                mobile=customer.contact_no,
                                subject=subject or "General Grievance",
                                category=category,
                                priority=priority,
                                description=description,
                                attachment=attachment,
                                status="Pending",
                            )
                            GrievanceHistory.objects.create(
                                grievance=grievance,
                                status="Pending",
                                remarks="Grievance submitted successfully.",
                            )
                            ticket_no = grievance.ticket_no
                            request.session.pop("grievance_customer_id", None)
                            request.session.pop("grievance_aadhaar_verified", None)
                            message = "Grievance registered successfully."
                            customer = None
                            applications = []

    return render(request, "raise_grievance.html", {
        "customer": customer,
        "applications": applications,
        "ticket_no": ticket_no,
        "message": message,
        "error": error,
    })


def grievance_status(request):
    """Supports both ticket-number tracking and the existing Aadhaar lookup flow."""
    grievance = None
    history = []
    customer = None
    grievances = []
    error = None
    ticket_no = (request.GET.get("ticket_no") or "").strip()
    aadhaar_no = (request.GET.get("aadhaar_no") or "").strip()

    if ticket_no:
        grievance = Grievance.objects.filter(ticket_no=ticket_no).select_related("application").first()
        if grievance:
            history = grievance.history.order_by("created_at")
        else:
            error = "Grievance ticket not found. Please check the ticket number."
    elif aadhaar_no:
        customer = Customer.objects.filter(aadhaar_no=aadhaar_no).first()
        if customer:
            grievances = Grievance.objects.filter(customer=customer).select_related("application").prefetch_related("history").order_by("-created_at")
        else:
            error = "Aadhaar number not found. Please check and try again."

    return render(request, "grievance_status.html", {
        "grievance": grievance,
        "history": history,
        "customer": customer,
        "grievances": grievances,
        "error": error,
        "ticket_no": ticket_no,
    })


def my_grievances(request):
    mobile = (request.GET.get("mobile") or "").strip()
    grievances = Grievance.objects.none()
    if mobile:
        grievances = Grievance.objects.filter(mobile=mobile).order_by("-created_at")
    return render(request, "my_grievances.html", {"grievances": grievances, "mobile": mobile})


# -----------------------------------------------------------------------------
# ADMIN LOGIN / HOME PAGE
# -----------------------------------------------------------------------------

def user_login(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            return redirect("/admin/")
        return render(request, "login.html", {"error": "Invalid credentials or admin access not permitted."})
    return render(request, "login.html")


def home(request):
    notices = Notice.objects.filter(active=True).order_by("-created_at")
    links = [
        {"name": "Admin Login", "url": "/admin/", "icon": "🔐"},
        {"name": "Customer Login", "url": "/customer-login/", "icon": "👤"},
        {"name": "Check Application Status", "url": "/check-status/", "icon": "🔎"},
        {"name": "Raise Grievance", "url": "/raise-grievance/", "icon": "📢"},
        {"name": "Track Grievance", "url": "/grievance-status/", "icon": "🎫"},
        {"name": "My Grievances", "url": "/my-grievances/", "icon": "📋"},
    ]
    return render(request, "home.html", {"notices": notices, "links": links})


# -----------------------------------------------------------------------------
# PASSWORD RESET
# -----------------------------------------------------------------------------

def customer_forgot_password(request):
    if request.method == "POST":
        aadhaar_no = (request.POST.get("aadhaar_no") or "").strip()
        contact_no = (request.POST.get("contact_no") or "").strip()
        new_password = request.POST.get("new_password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        if len(new_password) < 6:
            return render(request, "customer_forgot_password.html", {"error": "Password must be at least 6 characters."})
        if new_password != confirm_password:
            return render(request, "customer_forgot_password.html", {"error": "Password and Confirm Password do not match."})

        customer = Customer.objects.filter(aadhaar_no=aadhaar_no, contact_no=contact_no).select_related("user").first()
        if customer is None:
            return render(request, "customer_forgot_password.html", {"error": "Aadhaar number or mobile number is incorrect."})
        if not customer.user:
            return render(request, "customer_forgot_password.html", {"error": "No login account found for this customer."})

        customer.user.set_password(new_password)
        customer.user.save(update_fields=["password"])
        return redirect("/customer-login/?reset=1")

    return render(request, "customer_forgot_password.html")


# -----------------------------------------------------------------------------
# KRIPAROHII / CHAT API ENDPOINTS
# -----------------------------------------------------------------------------

def ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"reply": "Invalid JSON request."}, status=400)
    user_message = str(data.get("message", ""))[:1000]
    return JsonResponse({"reply": f"ACZ AI: Aapne bola - {user_message}"})


def kriparohii_verify(request):
    aadhaar = (request.GET.get("aadhaar") or "").strip()
    if not aadhaar:
        return JsonResponse({"success": False, "message": "Aadhaar missing"}, status=400)
    customer = Customer.objects.filter(aadhaar_no=aadhaar).first()
    if customer is None:
        return JsonResponse({"success": False, "message": "Customer not found"}, status=404)
    applications = customer.applications.all().values("application_name", "status")
    return JsonResponse({"success": True, "customer": customer.name, "applications": list(applications)})


def kriparohii_status(request):
    aadhaar = (request.GET.get("aadhaar") or "").strip()
    if not aadhaar:
        return JsonResponse({"success": False, "message": "Aadhaar required"}, status=400)
    customer = Customer.objects.filter(aadhaar_no=aadhaar).first()
    if customer is None:
        return JsonResponse({"success": False, "message": "Customer not found"}, status=404)

    applications = []
    for app in customer.applications.all().order_by("-application_date", "-id"):
        timeline = [{
            "status": item.status,
            "date": item.updated_at.strftime("%d-%m-%Y %H:%M"),
            "remarks": item.remark,
        } for item in app.status_history.order_by("updated_at")]
        applications.append({
            "application_name": app.application_name,
            "application_no": app.application_no,
            "status": app.status,
            "remarks": app.remarks,
            "timeline": timeline,
        })

    # Aadhaar is used for lookup only; it is not echoed back in the API response.
    return JsonResponse({
        "success": True,
        "customer": {"name": customer.name, "mobile": customer.contact_no},
        "applications": applications,
    })


def kriparohii_chat(request):
    msg = (request.GET.get("message") or "").strip()
    if msg == "Application Status":
        return JsonResponse({
            "reply": "📄 Application Status",
            "message": "Application status dekhne ke liye apna registered Aadhaar number verify karein.",
        })
    if msg == "Payment":
        return JsonResponse({"reply": "💳 Payment", "message": "Payment history dekhne ke liye Payment History page use karein."})
    if msg == "Grievance":
        return JsonResponse({"reply": "🎫 Grievance Status", "message": "Apna grievance ticket number enter karke status track karein."})
    if msg == "Notices":
        notices = Notice.objects.filter(active=True).order_by("-created_at").values("title", "message")[:10]
        return JsonResponse({"reply": "📢 Latest Notices", "data": list(notices)})
    return JsonResponse({"reply": "🤖 Kriparohii samajh nahi paayi."})


def kriparohii_grievance(request):
    aadhaar = (request.GET.get("aadhaar") or "").strip()
    if not aadhaar:
        return JsonResponse({"success": False, "message": "Aadhaar required"}, status=400)
    customer = Customer.objects.filter(aadhaar_no=aadhaar).first()
    if customer is None:
        return JsonResponse({"success": False, "message": "Customer not found"}, status=404)
    grievances = Grievance.objects.filter(customer=customer).values(
        "ticket_no", "category", "status", "priority", "remarks"
    ).order_by("-created_at")
    return JsonResponse({"success": True, "grievances": list(grievances)})


# -----------------------------------------------------------------------------
# LEGACY UPI VIEW
# -----------------------------------------------------------------------------
# Existing UPI submissions are retained for historical/admin records. This view
# intentionally no longer accepts new customer UTR submissions; customer Pay Now
# should route to the PayU create_payment view instead.
@login_required
def upi_payment(request, app_id):
    application = get_object_or_404(Application, id=app_id, customer__user=request.user)
    messages.info(request, "Manual UPI submissions are no longer accepted. Please use the Pay Now option for online payment.")
    return redirect("create_payment", app_id=application.id)
