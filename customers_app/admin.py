from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html

from .models import Customer, Application, ApplicationStatusHistory


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
        'status_updated_at',
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

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_obj = Application.objects.get(pk=obj.pk)
            old_status = old_obj.status

        super().save_model(request, obj, form, change)

        if not change or old_status != obj.status:
            ApplicationStatusHistory.objects.create(
                application=obj,
                status=obj.status,
                remark=obj.remarks
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

        ApplicationStatusHistory.objects.create(
            application=application,
            status='Delivered',
            remark=application.remarks
        )

        return redirect('/admin/customers_app/application/')


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'status', 'updated_at')