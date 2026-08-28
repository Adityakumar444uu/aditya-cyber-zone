from .models import Customer
import json
from django.http import JsonResponse
import hashlib
import time
import razorpay
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .google_sheet import sync_application_to_sheet

from .models import (
    Customer,
    Application,
    ApplicationStatusHistory,
    PaymentHistory,
    Grievance,
    GrievanceHistory,
    Notice,
)


def customer_list(request):
    customers = Customer.objects.all().order_by("-id")
    recent_applications = Application.objects.all().order_by("-id")[:5]
    recent_grievances = Grievance.objects.all().order_by("-id")[:5]

    return render(request, "customer_list.html", {
        "customers": customers,
        "recent_applications": recent_applications,
        "recent_grievances": recent_grievances,
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
        "open_grievances": Grievance.objects.exclude(status="Resolved").count(),
        "resolved_grievances": Grievance.objects.filter(status="Resolved").count(),
    })


def all_applications(request):
    status = request.GET.get("status")

    if status:
        applications = Application.objects.filter(status=status).order_by("-application_date")
    else:
        applications = Application.objects.all().order_by("-application_date")

    return render(request, "all_applications.html", {
        "applications": applications,
        "selected_status": status
    })


def add_application(request):
    customers = Customer.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer")
        customer = Customer.objects.get(id=customer_id)

        application = Application.objects.create(
            customer=customer,
            application_name=request.POST.get("application_name"),
            application_no=request.POST.get("application_no"),
            application_date=timezone.now().date(),
            status=request.POST.get("status") or "Pending"
        )

        sync_application_to_sheet(application)

        return redirect("all_applications")

    return render(request, "add_application.html", {
        "customers": customers
    })


def update_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        remark = request.POST.get("remark") or request.POST.get("remarks") or ""

        application.status = new_status
        application.remarks = remark

        if new_status == "Delivered":
            application.delivery_date = timezone.now()
        else:
            application.delivery_date = None

        application.save()

        ApplicationStatusHistory.objects.create(
            application=application,
            status=new_status,
            remark=remark
        )

        sync_application_to_sheet(application, remark)

    return redirect("all_applications")


def check_status(request):
    application = None
    error = None
    application_no = request.GET.get("application_no")

    if application_no:
        try:
            application = Application.objects.get(application_no=application_no)
        except Application.DoesNotExist:
            error = "Application Not Found"

    return render(request, "check_status.html", {
        "application": application,
        "error": error
    })


def customer_register(request):
    message = ""
    customer = None

    if request.method == "POST":

        # STEP 1 : Aadhaar Verify
        if "verify" in request.POST:
            aadhaar_no = request.POST.get("aadhaar_no")

            try:
                customer = Customer.objects.get(aadhaar_no=aadhaar_no)

                if customer.user:
                    message = "Account already created. Please login."

                else:
                    return render(request, "customer_register.html", {
                        "customer": customer,
                        "verified": True
                    })

            except Customer.DoesNotExist:
                message = "Aadhaar not found. Please contact Admin."

        # STEP 2 : Create Login Account
        elif "register" in request.POST:

            aadhaar_no = request.POST.get("aadhaar_no")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            try:
                customer = Customer.objects.get(aadhaar_no=aadhaar_no)

                if customer.user:
                    message = "Account already exists."

                elif password != confirm_password:
                    return render(request, "customer_register.html", {
                        "customer": customer,
                        "verified": True,
                        "message": "Password does not match."
                    })

                else:
                    user = User.objects.create_user(
                        username=customer.aadhaar_no,
                        password=password,
                        first_name=customer.name
                    )

                    customer.user = user
                    customer.save()

                    return redirect("/customer-login/?registered=1")

            except Customer.DoesNotExist:
                message = "Customer not found."

    return render(request, "customer_register.html", {
        "message": message,
        "customer": customer
    })
def customer_login(request):
    error = None

    if request.method == "POST":
        aadhaar_no = request.POST.get("aadhaar_no")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=aadhaar_no,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("customer_dashboard")
        else:
            error = "Invalid Aadhaar Number or Password."

    return render(request, "customer_login.html", {
        "error": error
    })

@login_required
def customer_dashboard(request):
    customer = Customer.objects.get(user=request.user)

    applications = Application.objects.filter(
        customer=customer
    ).order_by("-application_date")

    total_amount = sum(app.amount for app in applications)
    total_paid = sum(app.paid_amount for app in applications)
    total_due = sum(app.due_amount for app in applications)

    return render(request, "customer_dashboard.html", {
        "customer": customer,
        "applications": applications,
        "total_amount": total_amount,
        "total_paid": total_paid,
        "total_due": total_due,
    })


@login_required
def create_payment(request, app_id):
    application = get_object_or_404(
        Application,
        id=app_id,
        customer__user=request.user
    )

    if application.payment_status == "Paid":
        return redirect("receipt", app_id=application.id)

    if application.due_amount <= 0:
        return redirect("customer_dashboard")

    amount = "%.2f" % application.due_amount
    txnid = f"ACZ{application.id}{int(time.time())}"

    firstname = application.customer.name
    email = "support@adityacyberzone.com"
    phone = application.customer.contact_no
    productinfo = application.application_name

    hash_string = (
        f"{settings.PAYU_MERCHANT_KEY}|{txnid}|{amount}|{productinfo}|"
        f"{firstname}|{email}|||||||||||{settings.PAYU_MERCHANT_SALT}"
    )

    payu_hash = hashlib.sha512(
        hash_string.encode("utf-8")
    ).hexdigest().lower()

    application.razorpay_order_id = txnid
    application.save()

    payu_data = {
        "key": settings.PAYU_MERCHANT_KEY,
        "txnid": txnid,
        "amount": amount,
        "productinfo": productinfo,
        "firstname": firstname,
        "email": email,
        "phone": phone,
        "surl": request.build_absolute_uri(f"/payment-success/{application.id}/"),
        "furl": request.build_absolute_uri(f"/payment-success/{application.id}/"),
        "hash": payu_hash,
        "service_provider": "payu_paisa",
    }

    return render(request, "pay_now.html", {
        "application": application,
        "payu_data": payu_data,
        "payu_url": settings.PAYU_BASE_URL,
    })


@csrf_exempt
def payment_success(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if application.payment_status == "Paid":
        return redirect("receipt", app_id=application.id)

    status = request.POST.get("status")
    txnid = request.POST.get("txnid")
    mihpayid = request.POST.get("mihpayid")

    if status != "success":
        return render(request, "payment_failed.html", {
            "message": "Payment failed or cancelled."
        })

    application.paid_amount = application.amount
    application.due_amount = 0
    application.payment_status = "Paid"
    application.payment_mode = "Online"
    application.razorpay_payment_id = mihpayid
    application.razorpay_order_id = txnid
    application.save()

    already_exists = PaymentHistory.objects.filter(
        application=application,
        payment_reference_no=application.payment_reference_no
    ).exists()

    if not already_exists:
        PaymentHistory.objects.create(
            application=application,
            amount=application.amount,
            payment_mode="Online",
            payment_status="Paid",
            payment_reference_no=application.payment_reference_no,
            receipt_no=application.receipt_no,
        )


    return render(request, "payment_success.html", {
        "application": application
    })


@login_required
def payment_history(request):
    customer = Customer.objects.get(user=request.user)

    history = PaymentHistory.objects.filter(
        application__customer=customer
    ).order_by("-created_at")

    return render(request, "payment_history.html", {
        "history": history
    })


@login_required
def receipt(request, app_id):
    application = get_object_or_404(
        Application,
        id=app_id,
        customer__user=request.user
    )

    return render(request, "receipt.html", {
        "application": application
    })


def raise_grievance(request):
    ticket_no = None

    if request.method == "POST":
        grievance = Grievance.objects.create(
            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            category=request.POST.get("category"),
            priority=request.POST.get("priority"),
            description=request.POST.get("description"),
        )

        GrievanceHistory.objects.create(
            grievance=grievance,
            status="Pending",
            remarks="Grievance submitted successfully."
        )

        ticket_no = grievance.ticket_no

    return render(request, "raise_grievance.html", {
        "ticket_no": ticket_no
    })


def grievance_status(request):
    grievance = None
    history = []
    ticket_no = request.GET.get("ticket_no")

    if ticket_no:
        grievance = Grievance.objects.filter(ticket_no=ticket_no).first()

        if grievance:
            history = GrievanceHistory.objects.filter(
                grievance=grievance
            ).order_by("created_at")

    return render(request, "grievance_status.html", {
        "grievance": grievance,
        "history": history
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("/admin/")

    return render(request, "login.html")


def customer_logout(request):
    logout(request)
    return redirect("/customer-login/?success=1")


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

    return render(request, "home.html", {
        "notices": notices,
        "links": links,
    })


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    applications = Application.objects.filter(customer=customer)

    return render(request, "customer_detail.html", {
        "customer": customer,
        "applications": applications
    })


def my_grievances(request):
    grievances = []
    mobile = request.GET.get("mobile")

    if mobile:
        grievances = Grievance.objects.filter(
            mobile=mobile
        ).order_by("-created_at")

    return render(request, "my_grievances.html", {
        "grievances": grievances,
        "mobile": mobile
    })


def bulk_update_status(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_applications")
        new_status = request.POST.get("bulk_status")
        remark = request.POST.get("bulk_remark") or ""

        if selected_ids and new_status:
            applications = Application.objects.filter(id__in=selected_ids)

            for application in applications:
                application.status = new_status
                application.remarks = remark
                 

                if new_status == "Delivered":
                    application.delivery_date = timezone.now()
                else:
                    application.delivery_date = None

                application.save()

                ApplicationStatusHistory.objects.create(
                    application=application,
                    status=new_status,
                    remark=remark
                )

                sync_application_to_sheet(application, remark)

    return redirect("all_applications")
def customer_forgot_password(request):
    if request.method == "POST":
        aadhaar_no = request.POST.get("aadhaar_no")
        contact_no = request.POST.get("contact_no")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, "customer_forgot_password.html", {
                "error": "Password and Confirm Password do not match."
            })

        try:
            customer = Customer.objects.get(
                aadhaar_no=aadhaar_no,
                contact_no=contact_no
            )

            if not customer.user:
                return render(request, "customer_forgot_password.html", {
                    "error": "No login account found for this customer."
                })

            customer.user.set_password(new_password)
            customer.user.save()

            return redirect("/customer-login/?reset=1")

        except Customer.DoesNotExist:
            return render(request, "customer_forgot_password.html", {
                "error": "Aadhaar number or mobile number is incorrect."
            })

    return render(request, "customer_forgot_password.html")
def ai_chat(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user_message = data.get("message")

        reply = f"ACZ AI: Aapne bola - {user_message}"

        return JsonResponse({
            "reply": reply
        })

    return JsonResponse({
        "reply": "Invalid request"
    })
def kriparohii_verify(request):

    aadhaar = request.GET.get("aadhaar")

    if not aadhaar:
        return JsonResponse({
            "success":False,
            "message":"Aadhaar missing"
        })


    try:

        customer = Customer.objects.get(
            aadhaar_no=aadhaar
        )


        applications = customer.application_set.all()

        app_list = []


        for app in applications:

            app_list.append({
                "name": app.application_name,
                "status": app.status
            })


        return JsonResponse({

            "success": True,
            "customer": customer.name,
            "applications": app_list

        })


    except Customer.DoesNotExist:

        return JsonResponse({

            "success": False,
            "message": "Customer not found"

        })
from django.http import JsonResponse
from .models import Customer, Application

def kriparohii_status(request):

    aadhaar = request.GET.get("aadhaar")

    if not aadhaar:
        return JsonResponse({
            "success": False,
            "message": "Aadhaar required"
        })


    try:
        customer = Customer.objects.get(
            aadhaar_no=aadhaar
        )


        applications = []

        for app in Application.objects.filter(customer=customer):

            timeline = []

            try:
                histories = app.applicationstatushistory_set.all().order_by("created_at")

                for h in histories:
                    timeline.append({
                        "status": h.status,
                        "date": h.created_at.strftime("%d-%m-%Y %H:%M"),
                        "remarks": h.remarks
                    })

            except:
                pass


            applications.append({

                "application_name": app.application_name,

                "application_no": app.application_no,

                "status": app.status,

                "remarks": app.remarks,

                "timeline": timeline

            })


        return JsonResponse({

            "success": True,

            "customer": {

                "name": customer.name,

                "mobile": customer.contact_no,

                "aadhaar": customer.aadhaar_no

            },

            "applications": applications

        })


    except Customer.DoesNotExist:

        return JsonResponse({

            "success": False,

            "message": "Customer not found"

        })
from django.http import JsonResponse
from .models import Application, Grievance, Notice


def kriparohii_chat(request):

    msg = request.GET.get("message","")


    if msg == "Application Status":

        apps = Application.objects.all().values(
            "application_name",
            "application_no",
            "status"
        )

        return JsonResponse({

            "reply":"📄 Application Status",

            "data":list(apps)

        })


    elif msg == "Payment":

        return JsonResponse({

            "reply":
            "💳 Payment check karne ke liye apna Application Number enter karein."

        })


    elif msg == "Grievance":

        grievances = Grievance.objects.all().values(
            "ticket_no",
            "status",
            "category"
        )

        return JsonResponse({

            "reply":"🎫 Grievance Status",

            "data":list(grievances)

        })


    elif msg == "Notices":

        notices = Notice.objects.all().values(
            "title",
            "message"
        )

        return JsonResponse({

            "reply":"📢 Latest Notices",

            "data":list(notices)

        })


    else:

        return JsonResponse({

            "reply":
            "🤖 Kriparohii samajh nahi paayi."

        })
def kriparohii_grievance(request):

    aadhaar = request.GET.get("aadhaar")

    if not aadhaar:
        return JsonResponse({
            "success":False,
            "message":"Aadhaar required"
        })

    try:
        customer = Customer.objects.get(
            aadhaar_no=aadhaar
        )

        grievances = Grievance.objects.filter(
            customer=customer
        ).values(
            "ticket_no",
            "category",
            "status",
            "priority",
            "remarks"
        )

        return JsonResponse({
            "success":True,
            "grievances":list(grievances)
        })

    except Customer.DoesNotExist:
        return JsonResponse({
            "success":False,
            "message":"Customer not found"
        })
