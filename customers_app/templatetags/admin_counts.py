from django import template
from customers_app.models import Customer, Application

register = template.Library()

@register.simple_tag
def total_customers():
    return Customer.objects.count()

@register.simple_tag
def total_applications():
    return Application.objects.count()

@register.simple_tag
def pending_applications():
    return Application.objects.filter(status="Pending").count()

@register.simple_tag
def delivered_applications():
    return Application.objects.filter(status="Delivered").count()