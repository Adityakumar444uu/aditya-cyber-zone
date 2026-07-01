from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import razorpay
from decimal import Decimal

from .excel_sync import sync_application_to_excel
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Customer,
    Application,
    ApplicationStatusHistory,
    PaymentHistory,
    Grievance,
    GrievanceHistory,
    Notice,
)
from .google_sheet import sync_application_to_sheet


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
    status = request.GET.get('status')

    if status:
        applications = Application.objects.filter(status=status).order_by('-application_date')
    else:
        applications = Application.objects.all().order_by('-application_date')

    return render(request, 'all_applications.html', {
        'applications': applications,
        'selected_status': status
    })


def add_application(request):
    customers = Customer.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(id=customer_id)

        application = Application.objects.create(
            customer=customer,
            application_name=request.POST.get('application_name'),
            application_no=request.POST.get('application_no'),
            application_date=timezone.now().date(),
            status=request.POST.get('status') or "Pending"
        )

        sync_application_to_sheet(application)
        sync_application_to_excel(application)

        return redirect('all_applications')

    return render(request, 'add_application.html', {
        'customers': customers
    })


def update_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        remark = request.POST.get('remark') or request.POST.get('remarks') or ""

        application.status = new_status
        application.remarks = remark

        if new_status == "Delivered":
            application.delivery_date = timezone.now()
        else:
            application.delivery_date = None

        application.save()
        sync_application_to_excel(application)

        ApplicationStatusHistory.objects.create(
            application=application,
            status=new_status,
            remark=remark
        )

        sync_application_to_sheet(application, remark)

    return redirect('all_applications')


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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        aadhaar_no = request.POST.get('aadhaar_no')
        contact_no = request.POST.get('contact_no')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Customer.objects.create(
            user=user,
            name=name,
            aadhaar_no=aadhaar_no,
            contact_no=contact_no
        )

        return redirect('/customer-login/?success=1')

    return render(request, 'customer_register.html')


def customer_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            error = "Invalid Username or Password"

    return render(request, 'customer_login.html', {
        'error': error
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

    return render(request, 'customer_dashboard.html', {
        'customer': customer,
        'applications': applications,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_due': total_due,
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

    amount_paise = int(application.due_amount * Decimal("100"))

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    try:
    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1,
        "notes": {
            "application_id": str(application.id),
            "application_no": application.application_no,
            "customer": application.customer.name,
        }
    })
except Exception as e:
    return HttpResponse(f"Razorpay Error: {str(e)}")
    application.razorpay_order_id = order["id"]
    application.save()

    return render(request, "pay_now.html", {
        "application": application,
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount_paise": amount_paise,
    })

@csrf_exempt
def payment_success(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if application.payment_status == "Paid":
        return redirect("receipt", app_id=application.id)

    payment_id = request.POST.get("razorpay_payment_id") or request.GET.get("payment_id")
    order_id = request.POST.get("razorpay_order_id") or request.GET.get("order_id")
    signature = request.POST.get("razorpay_signature") or request.GET.get("signature")

    if not payment_id or not order_id or not signature:
        return render(request, "payment_failed.html", {
            "message": "Payment details missing. Please contact admin."
        })

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
    except Exception:
        return render(request, "payment_failed.html", {
            "message": "Payment verification failed. Please contact admin."
        })

    application.paid_amount = application.amount
    application.due_amount = 0
    application.payment_status = "Paid"
    application.payment_mode = "Online"
    application.razorpay_payment_id = payment_id
    application.razorpay_order_id = order_id
    application.razorpay_signature = signature
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

    sync_application_to_excel(application)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/admin/')

    return render(request, 'login.html')


def customer_logout(request):
    logout(request)
    return redirect('/customer-login/?success=1')


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

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'applications': applications
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

                sync_application_to_excel(application)
                sync_application_to_sheet(application, remark)

    return redirect("all_applications")