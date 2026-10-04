from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    aadhaar_no = models.CharField(
        max_length=20,
        unique=True,
        db_index=True
    )

    contact_no = models.CharField(max_length=15)

    # Customer self registration status
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.aadhaar_no}"


class ApplicationPart(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ApplicationSubPart(models.Model):
    part = models.ForeignKey(
        ApplicationPart,
        on_delete=models.CASCADE,
        related_name="subparts"
    )

    name = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        unique_together = ("part", "name")

    def __str__(self):
        return f"{self.part.name} - {self.name} ₹{self.amount}"


class Application(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Submitted", "Submitted"),
        ("In Process", "In Process"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Delivered", "Delivered"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("Cash", "Cash"),
        ("Online", "Online"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    part = models.ForeignKey(
        ApplicationPart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sub_part = models.ForeignKey(
        ApplicationSubPart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    application_name = models.CharField(
        max_length=100
    )

    application_no = models.CharField(
        max_length=100
    )

    application_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    due_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Unpaid"
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        default="Cash"
    )

    payment_reference_no = models.CharField(
        max_length=50,
        unique=False,
        blank=True,
        null=True
    )

    receipt_no = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    status_updated_at = models.DateTimeField(
        auto_now=True
    )

    delivery_date = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.sub_part:
            self.part = self.sub_part.part
            self.amount = self.sub_part.amount
            self.application_name = self.sub_part.name

        self.due_amount = self.amount - self.paid_amount

        if self.due_amount < 0:
            self.due_amount = 0

        if self.paid_amount >= self.amount and self.amount > 0:
            self.payment_status = "Paid"

            count = Application.objects.count() + 1

            if not self.payment_reference_no:
                self.payment_reference_no = (
                    f"ACZPAY"
                    f"{timezone.now().strftime('%Y%m%d')}"
                    f"{count:04d}"
                )

            if not self.receipt_no:
                self.receipt_no = (
                    f"RCPT-"
                    f"{timezone.now().strftime('%Y%m%d')}-"
                    f"{count:04d}"
                )

        else:
            self.payment_status = "Unpaid"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.application_name


class ApplicationStatusHistory(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    status = models.CharField(
        max_length=50
    )

    remark = models.TextField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.application} - {self.status}"


class PaymentHistory(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="payment_history"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20
    )

    payment_status = models.CharField(
        max_length=20
    )

    payment_reference_no = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    receipt_no = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.application} - ₹{self.amount}"


class Grievance(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Process", "In Process"),
        ("Waiting for Customer", "Waiting for Customer"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
        ("Closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    customer = models.ForeignKey(
    Customer,
    on_delete=models.CASCADE,
    related_name="grievances",
    null=True,
    blank=True
)

    # The exact application against which the grievance is raised
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grievances"
    )

    ticket_no = models.CharField(
        max_length=40,
        unique=True,
        blank=True
    )

    # Snapshot fields for safe display/history
    name = models.CharField(
        max_length=100
    )

    mobile = models.CharField(
        max_length=15
    )

    subject = models.CharField(
        max_length=200,
        default="General Grievance"
    )

    category = models.CharField(
        max_length=100
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )

    description = models.TextField()

    attachment = models.FileField(
        upload_to="grievances/%Y/%m/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    closed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        # If application is selected, always use its customer.
        if self.application:
            self.customer = self.application.customer

        # Automatically keep snapshot customer details updated.
        if self.customer:
            self.name = self.customer.name
            self.mobile = self.customer.contact_no

        # Generate ticket number only once.
        if not self.ticket_no:
            today = timezone.now().strftime("%Y%m%d")

            while True:
                random_part = uuid.uuid4().hex[:6].upper()
                ticket = f"GRV-{today}-{random_part}"

                if not Grievance.objects.filter(
                    ticket_no=ticket
                ).exists():
                    self.ticket_no = ticket
                    break

        # Automatically maintain resolution/closure timestamps.
        if self.status == "Resolved":
            if not self.resolved_at:
                self.resolved_at = timezone.now()
        else:
            self.resolved_at = None

        if self.status == "Closed":
            if not self.closed_at:
                self.closed_at = timezone.now()
        else:
            self.closed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_no


class GrievanceHistory(models.Model):

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name="history"
    )

    status = models.CharField(
        max_length=50
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.grievance.ticket_no} - {self.status}"


class GrievanceMessage(models.Model):

    SENDER_CHOICES = [
        ("Customer", "Customer"),
        ("Admin", "Admin"),
    ]

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender_type = models.CharField(
        max_length=20,
        choices=SENDER_CHOICES
    )

    message = models.TextField()

    attachment = models.FileField(
        upload_to="grievance_messages/%Y/%m/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.grievance.ticket_no} - "
            f"{self.sender_type}"
        )


class Notice(models.Model):

    PRIORITY = [
        ("Normal", "Normal"),
        ("Important", "Important"),
        ("Urgent", "Urgent"),
    ]

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="Normal"
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title