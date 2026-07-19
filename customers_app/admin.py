import os
from django.conf import settings
from django.core import serializers
from django.http import FileResponse
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html

#from .excel_sync import sync_application_to_excel

from .models import (
    Notice,
    Customer,
    ApplicationPart,
    ApplicationSubPart,
    Application,
    ApplicationStatusHistory,
    PaymentHistory,
    Grievance,
    GrievanceHistory,
)


@admin.register(ApplicationPart)
class ApplicationPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ApplicationSubPart)
class ApplicationSubPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'part', 'name', 'amount')
    list_filter = ('part',)
    search_fields = ('name', 'part__name')


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    fields = (
        'part',
        'sub_part',
        'application_no',
        'application_date',
        'amount',
        'paid_amount',
        'due_amount',
        'payment_status',
        'payment_mode',
        'payment_reference_no',
        'receipt_no',
        'status',
        'delivery_date',
        'remarks',
    )
    readonly_fields = (
        'amount',
        'due_amount',
        'payment_status',
        'payment_reference_no',
        'receipt_no',
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'aadhaar_no', 'contact_no')
    search_fields = ('name', 'aadhaar_no', 'contact_no')
    inlines = [ApplicationInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    change_list_template = "admin/customers_app/application/change_list.html"
    save_on_top = True

    list_display = (
        'id',
        'customer',
        'service_info',
        'application_no',
        'payment_info',
        'status',
        'remarks_short',
        'mark_delivered_button',
    )
    list_editable = ('status',)
    list_filter = ('payment_status', 'payment_mode', 'status', 'part', 'sub_part')
    search_fields = (
        'application_name',
        'application_no',
        'payment_reference_no',
        'receipt_no',
        'customer__name',
        'customer__aadhaar_no',
        'customer__contact_no',
        'part__name',
        'sub_part__name',
    )

    readonly_fields = (
        'amount',
        'due_amount',
        'payment_status',
        'payment_reference_no',
        'receipt_no',
        'status_updated_at',
    )

    list_per_page = 20
    list_max_show_all = 50
    date_hierarchy = "status_updated_at"
    save_on_top = True

    fieldsets = (
        ("Customer & Application", {
            "fields": (
                "customer",
                "part",
                "sub_part",
                "application_no",
                "application_date",
            )
        }),
        ("Payment", {
            "fields": (
                "amount",
                "paid_amount",
                "due_amount",
                "payment_status",
                "payment_mode",
                "payment_reference_no",
                "receipt_no",
            )
        }),
        ("Status", {
            "fields": (
                "status",
                "delivery_date",
                "remarks",
                "status_updated_at",
            )
        }),
    )

    class Media:
        css = {
            "all": ("admin_custom/application_admin.css",)
        }

    def service_info(self, obj):
        return format_html(
            "<b>{}</b><br><small>{}</small>",
            obj.part,
            obj.sub_part
        )
    service_info.short_description = "Service"

    def payment_info(self, obj):
        return format_html(
            "₹{}<br><small>Paid ₹{} | Due ₹{}<br>{} / {}</small>",
            obj.amount,
            obj.paid_amount,
            obj.due_amount,
            obj.payment_status,
            obj.payment_mode,
        )
    payment_info.short_description = "Payment"

    def remarks_short(self, obj):
        if obj.remarks:
            return obj.remarks[:25] + "..." if len(obj.remarks) > 25 else obj.remarks
        return "-"
    remarks_short.short_description = "Remarks"

    def save_model(self, request, obj, form, change):
        old_status = None
        old_paid_amount = 0

        if change:
            old_obj = Application.objects.get(pk=obj.pk)
            old_status = old_obj.status
            old_paid_amount = old_obj.paid_amount

        if obj.status == 'Delivered' and not obj.delivery_date:
            obj.delivery_date = timezone.now()

        super().save_model(request, obj, form, change)

     #   sync_application_to_excel(obj)

        if obj.paid_amount > old_paid_amount:
            PaymentHistory.objects.create(
                application=obj,
                amount=obj.paid_amount - old_paid_amount,
                payment_mode=obj.payment_mode,
                payment_status=obj.payment_status,
                payment_reference_no=obj.payment_reference_no,
                receipt_no=obj.receipt_no,
            )

        if not change or old_status != obj.status:
            ApplicationStatusHistory.objects.create(
                application=obj,
                status=obj.status,
                remark=obj.remarks,
            )

    def mark_delivered_button(self, obj):
        if obj.status != 'Delivered':
            return format_html(
                '<a class="button" href="mark-delivered/{}/">Delivered</a>',
                obj.id,
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

        # Excel sync removed

        ApplicationStatusHistory.objects.create(
            application=application,
            status='Delivered',
            remark=application.remarks,
        )

        return redirect('/admin/customers_app/application/')
@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'status', 'updated_at')
    search_fields = ('application__application_name', 'status')


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'application',
        'amount',
        'payment_mode',
        'payment_status',
        'payment_reference_no',
        'receipt_no',
        'created_at',
    )
    list_filter = ('payment_mode', 'payment_status', 'created_at')
    search_fields = (
        'application__application_name',
        'application__application_no',
        'payment_reference_no',
        'receipt_no',
    )


@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ticket_no',
        'name',
        'mobile',
        'category',
        'priority',
        'status',
        'created_at',
    )
    list_editable = ('status',)
    list_filter = ('status', 'priority', 'category')
    search_fields = ('ticket_no', 'name', 'mobile')


@admin.register(GrievanceHistory)
class GrievanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('grievance', 'status', 'created_at')


old_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}

    extra_context["total_customers"] = Customer.objects.count()
    extra_context["total_applications"] = Application.objects.count()

    extra_context["pending_count"] = Application.objects.filter(status="Pending").count()
    extra_context["submitted_count"] = Application.objects.filter(status="Submitted").count()
    extra_context["in_process_count"] = Application.objects.filter(status="In Process").count()
    extra_context["approved_count"] = Application.objects.filter(status="Approved").count()
    extra_context["rejected_count"] = Application.objects.filter(status="Rejected").count()
    extra_context["delivered_count"] = Application.objects.filter(status="Delivered").count()

    extra_context["paid_count"] = Application.objects.filter(payment_status="Paid").count()
    extra_context["unpaid_count"] = Application.objects.filter(payment_status="Unpaid").count()

    extra_context["total_collection"] = sum(app.paid_amount for app in Application.objects.all())
    extra_context["total_due"] = sum(app.due_amount for app in Application.objects.all())

    extra_context["cash_collection"] = sum(
        app.paid_amount for app in Application.objects.filter(payment_mode="Cash")
    )
    extra_context["online_collection"] = sum(
        app.paid_amount for app in Application.objects.filter(payment_mode="Online")
    )

    extra_context["total_grievances"] = Grievance.objects.count()
    extra_context["grievance_pending"] = Grievance.objects.filter(status="Pending").count()
    extra_context["grievance_resolved"] = Grievance.objects.filter(status="Resolved").count()

    return old_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index


def backup_database(request):
    backup_file = os.path.join(settings.BASE_DIR, "acz_full_backup.json")

    data = serializers.serialize(
        "json",
        list(Customer.objects.all()) +
        list(ApplicationPart.objects.all()) +
        list(ApplicationSubPart.objects.all()) +
        list(Application.objects.all()) +
        list(ApplicationStatusHistory.objects.all()) +
        list(PaymentHistory.objects.all()) +
        list(Grievance.objects.all()) +
        list(GrievanceHistory.objects.all()),
        indent=4
    )

    with open(backup_file, "w", encoding="utf-8") as f:
        f.write(data)

    return FileResponse(
        open(backup_file, "rb"),
        as_attachment=True,
        filename="acz_full_backup.json"
    )


old_get_urls = admin.site.get_urls


def custom_get_urls():
    urls = old_get_urls()
    custom_urls = [
        path(
            "backup-database/",
            admin.site.admin_view(backup_database),
            name="backup_database"
        ),
    ]
    return custom_urls + urls


admin.site.get_urls = custom_get_urls


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'active', 'created_at')
    list_editable = ('active',)
    list_filter = ('priority', 'active')
    search_fields = ('title', 'message')