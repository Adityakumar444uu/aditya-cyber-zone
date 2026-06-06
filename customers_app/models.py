from django.db import models
from django.contrib.auth.models import User


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


class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('In Process', 'In Process'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    application_name = models.CharField(max_length=100)
    application_no = models.CharField(max_length=100)
    application_date = models.DateField()
    status_updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    remarks = models.TextField(blank=True)

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


class Grievance(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ticket_no = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    subject = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_no:
            last_id = Grievance.objects.count() + 1
            self.ticket_no = f"ACZ-GR-{last_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_no
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

    ticket_no = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    category = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Normal")
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_no:
            last_id = Grievance.objects.count() + 1
            self.ticket_no = f"GRV-{last_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_no


class GrievanceHistory(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status