from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError

def generate_unique_payment_reference():
    """Generate a payment reference not already used in Payment History."""
    while True:
        value = (
            f"ACZPAY-{timezone.now():%Y%m%d}-"
            f"{uuid.uuid4().hex.upper()}"
        )
        if not PaymentHistory.objects.filter(
            payment_reference_no=value
        ).exists():
            return value


def generate_unique_receipt_no():
    """Generate a receipt number not already used in Payment History."""
    while True:
        value = (
            f"RCPT-{timezone.now():%Y%m%d}-"
            f"{uuid.uuid4().hex.upper()}"
        )
        if not PaymentHistory.objects.filter(receipt_no=value).exists():
            return value

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

    service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    @property
    def total_amount(self):
        return (self.amount or 0) + (self.service_charge or 0)

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
        # Fully paid application ke financial details lock rahenge.
        if self.pk:
            old = Application.objects.filter(pk=self.pk).first()

            if old and old.payment_status == "Paid":
                locked_fields = [
                    "amount",
                    "service_charge",
                    "paid_amount",
                    "due_amount",
                    "payment_status",
                    "payment_mode",
                    "payment_reference_no",
                    "receipt_no",
                    "sub_part_id",
                    "part_id",
                ]

                changed_fields = [
                    field for field in locked_fields
                    if getattr(self, field) != getattr(old, field)
                ]

                if changed_fields:
                    raise ValidationError(
                        "This application is fully paid. "
                        "Its payment details are locked."
                    )

        if self.sub_part:
            self.part = self.sub_part.part
            self.amount = self.sub_part.amount
            self.application_name = self.sub_part.name

        self.due_amount = self.total_amount - self.paid_amount

        if self.due_amount < 0:
            self.due_amount = 0

        if self.total_amount > 0 and self.paid_amount >= self.total_amount:
            self.payment_status = "Paid"

            if not self.payment_reference_no:
                self.payment_reference_no = generate_unique_payment_reference()

            if not self.receipt_no:
                self.receipt_no = generate_unique_receipt_no()
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

    def save(self, *args, **kwargs):
        # Existing payment record ko edit nahi kar sakte.
        if self.pk and PaymentHistory.objects.filter(pk=self.pk).exists():
            raise ValidationError(
                "Payment history records cannot be edited."
            )

        # Blank ya pehle se used IDs ko nayi unique IDs se replace karo.
        if (
            not self.payment_reference_no
            or PaymentHistory.objects.filter(
                payment_reference_no=self.payment_reference_no
            ).exists()
        ):
            self.payment_reference_no = generate_unique_payment_reference()

        if (
            not self.receipt_no
            or PaymentHistory.objects.filter(
                receipt_no=self.receipt_no
            ).exists()
        ):
            self.receipt_no = generate_unique_receipt_no()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(
            "Payment history records cannot be deleted."
        )



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

        # Check whether grievance is being changed to Closed
        closing_now = False

        if self.pk:
            old_grievance = Grievance.objects.filter(
                pk=self.pk
            ).only("status").first()

            if (
                old_grievance
                and old_grievance.status != "Closed"
                and self.status == "Closed"
            ):
                closing_now = True

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

        # Save grievance
        super().save(*args, **kwargs)

        # ---------------------------------------------
        # AUTO DELETE ATTACHMENTS WHEN GRIEVANCE CLOSES
        # ---------------------------------------------
        if closing_now:

            # Delete main grievance attachment
            if self.attachment:
                self.attachment.delete(save=False)

                Grievance.objects.filter(
                    pk=self.pk
                ).update(
                    attachment=None
                )

                self.attachment = None

            # Delete attachments from all grievance messages
            for message in self.messages.all():

                if message.attachment:
                    message.attachment.delete(save=False)

                    message.attachment = None

                    message.save(
                        update_fields=["attachment"]
                    )

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


from django.conf import settings as django_settings


class UpiPaymentSubmission(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending Verification"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="upi_payment_submissions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    utr = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    reviewed_by = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.utr} - {self.status}"
class PayUTransaction(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="payu_transactions"
    )
    txnid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    mihpayid = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.txnid} - {self.status}"

class PaymentNotification(models.Model):

    payu_transaction = models.OneToOneField(
        PayUTransaction,
        on_delete=models.CASCADE,
        related_name="notification"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    read_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"{self.payu_transaction.txnid} - {status}"


# CUSTOMER SESSION AND ACTIVITY MONITORING

class CustomerSession(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="monitoring_sessions",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["customer", "started_at"]),
            models.Index(fields=["is_active", "last_activity"]),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.started_at}"


class CustomerActivity(models.Model):
    EVENT_CHOICES = [
        ("REGISTER", "Registration"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("PAGE_VISIT", "Page Visit"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )
    session = models.ForeignKey(
        CustomerSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
    )
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    page_path = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["customer", "created_at"]),
            models.Index(fields=["event_type", "created_at"]),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.event_type}"
