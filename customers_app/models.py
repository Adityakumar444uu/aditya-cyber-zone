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