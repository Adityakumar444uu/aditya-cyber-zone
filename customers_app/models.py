from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    aadhaar_no = models.CharField(max_length=20, unique=True)
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.name


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
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("part", "name")

    def __str__(self):
        return f"{self.part.name} - {self.name} ₹{self.amount}"


class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('In Process', 'In Process'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Delivered', 'Delivered'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("Cash", "Cash"),
        ("Online", "Online"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

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

    application_name = models.CharField(max_length=100)
    application_no = models.CharField(max_length=100)
    application_date = models.DateField()

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

    status_updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    remarks = models.TextField(blank=True)

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
                self.payment_reference_no = f"ACZPAY{timezone.now().strftime('%Y%m%d')}{count:04d}"

            if not self.receipt_no:
                self.receipt_no = f"RCPT-{timezone.now().strftime('%Y%m%d')}-{count:04d}"
        else:
            self.payment_status = "Unpaid"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.application_name


class ApplicationStatusHistory(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='status_history'
    )

    status = models.CharField(max_length=50)
    remark = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.status}"


class PaymentHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="payment_history"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    payment_reference_no = models.CharField(max_length=50, blank=True, null=True)
    receipt_no = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - ₹{self.amount}"


class Grievance(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Process", "In Process"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ticket_no = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    category = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_no:
            last_id = Grievance.objects.count() + 1
            self.ticket_no = f"GRV-{last_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_no


class GrievanceHistory(models.Model):
    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class Notice(models.Model):

    PRIORITY = [
        ("Normal", "Normal"),
        ("Important", "Important"),
        ("Urgent", "Urgent"),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="Normal"
    )

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title