from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html

from .models import Customer, Application


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    fields = (
        'application_name',
        'application_no',
        'application_date',
        'status',
        'delivery_date',
        'remarks',
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'aadhaar_no', 'contact_no')
    search_fields = ('name', 'aadhaar_no', 'contact_no')
    inlines = [ApplicationInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'application_name',
        'application_no',
        'status',
        'delivery_date',
        'mark_delivered_button',
    )

    list_filter = ('status',)
    search_fields = (
        'application_name',
        'application_no',
        'customer__name',
        'customer__aadhaar_no',
    )

    def mark_delivered_button(self, obj):
        if obj.status != 'Delivered':
            return format_html(
                '<a class="button" href="mark-delivered/{}/">Mark as Delivered</a>',
                obj.id
            )
        return "Delivered"

    mark_delivered_button.short_description = "Action"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'mark-delivered/<int:app_id>/',
                self.admin_site.admin_view(self.mark_delivered),
                name='mark_delivered',
            ),
        ]

        return custom_urls + urls

    def mark_delivered(self, request, app_id):
        application = Application.objects.get(id=app_id)
        application.status = 'Delivered'
        application.delivery_date = timezone.now()
        application.save()

        return redirect('/admin/customers_app/application/')