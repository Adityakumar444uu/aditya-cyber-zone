from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Application, ApplicationStatusHistory, Grievance, GrievanceHistory
from .google_sheet import sync_application_to_sheet


def customer_list(request):
    customers = Customer.objects.all()

    total_customers = Customer.objects.count()
    total_applications = Application.objects.count()

    pending_count = Application.objects.filter(status="Pending").count()
    submitted_count = Application.objects.filter(status="Submitted").count()
    in_process_count = Application.objects.filter(status="In Process").count()
    approved_count = Application.objects.filter(status="Approved").count()
    rejected_count = Application.objects.filter(status="Rejected").count()
    delivered_count = Application.objects.filter(status="Delivered").count()

    return render(request, "customer_list.html", {
        "customers": customers,
        "total_customers": total_customers,
        "total_applications": total_applications,
        "pending_count": pending_count,
        "submitted_count": submitted_count,
        "in_process_count": in_process_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "delivered_count": delivered_count,
        "pending_applications": pending_count,
        "delivered_applications": delivered_count,
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
            status=request.POST.get('status')
        )

        sync_application_to_sheet(application)

        return redirect('all_applications')

    return render(request, 'add_application.html', {
        'customers': customers
    })


def update_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        remark = request.POST.get('remark')

        application.status = new_status

        if new_status == "Delivered":
            application.delivery_date = timezone.now()

        application.save()

        ApplicationStatusHistory.objects.create(
            application=application,
            status=new_status,
            remark=remark
        )

        sync_application_to_sheet(application, remark)

    return redirect('all_applications')


def check_status(request):
    result = None
    error = None

    if request.method == "POST":
        application_no = request.POST.get("application_no")

        try:
            result = Application.objects.get(application_no=application_no)
        except Application.DoesNotExist:
            error = "Application not found"

    return render(request, 'check_status.html', {
        'result': result,
        'error': error
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
    applications = Application.objects.filter(customer=customer)

    return render(request, 'customer_dashboard.html', {
        'customer': customer,
        'applications': applications
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
def home(request):
    links = [
        {"name": "Admin Login", "url": "/admin/", "icon": "🔐"},
        {"name": "Customer Login", "url": "/customer-login/", "icon": "👤"},
        {"name": "Check Application Status", "url": "/check-status/", "icon": "🔎"},
        {"name": "Raise Grievance", "url": "/raise-grievance/", "icon": "📢"},
        {"name": "Track Grievance", "url": "/grievance-status/", "icon": "🎫"},
    ]

    return render(request, "home.html", {"links": links})
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
    links = [
        {"name": "Admin Login", "url": "/admin/", "icon": "🔐"},
        {"name": "Customer Login", "url": "/customer-login/", "icon": "👤"},
        {"name": "Check Application Status", "url": "/check-status/", "icon": "🔎"},
        {"name": "Raise Grievance", "url": "/raise-grievance/", "icon": "📢"},
        {"name": "Track Grievance", "url": "/grievance-status/", "icon": "🎫"},
    ]

    return render(request, "home.html", {"links": links})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    applications = Application.objects.filter(customer=customer)

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'applications': applications
    })