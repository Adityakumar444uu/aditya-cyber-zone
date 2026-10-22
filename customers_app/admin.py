import os

from django.conf import settings
from django.core import serializers
from django.http import FileResponse
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html

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
    UpiPaymentSubmission,
)
from django.db import transaction


# =========================
# SERVICE PART ADMIN
# =========================

@admin.register(ApplicationPart)
class ApplicationPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ApplicationSubPart)
class ApplicationSubPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'part', 'name', 'amount')
    list_filter = ('part',)
    search_fields = ('name', 'part__name')


# =========================
# CUSTOMER ADMIN
# =========================
\
class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    can_delete = True

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

    list_display = (
        'id',
        'name',
        'aadhaar_no',
        'contact_no'
    )

    search_fields = (
        'name',
        'aadhaar_no',
        'contact_no'
    )

    inlines = [ApplicationInline]


# =========================
# APPLICATION ADMIN
# =========================

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    change_list_template = (
        "admin/customers_app/application/change_list.html"
    )

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

    list_filter = (
        'payment_status',
        'payment_mode',
        'status',
        'part',
        'sub_part'
    )

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


        ("Payment Details", {
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
            "all": (
                "admin_custom/application_admin.css",
            )
        }


    def service_info(self,obj):

        return format_html(
            "<b>{}</b><br><small>{}</small>",
            obj.part,
            obj.sub_part
        )

    service_info.short_description = "Service"



    def payment_info(self,obj):

        return format_html(
            "₹{}<br><small>Paid ₹{} | Due ₹{}<br>{} / {}</small>",
            obj.amount,
            obj.paid_amount,
            obj.due_amount,
            obj.payment_status,
            obj.payment_mode,
        )

    payment_info.short_description = "Payment"



    def remarks_short(self,obj):

        if obj.remarks:
            return (
                obj.remarks[:25] + "..."
                if len(obj.remarks) > 25
                else obj.remarks
            )

        return "-"

    remarks_short.short_description = "Remarks"



    # =====================
    # FIXED SAVE MODEL
    # =====================

    def save_model(self, request, obj, form, change):

        old_status = None
        old_paid_amount = 0


        if change:

            old_obj = Application.objects.get(
                pk=obj.pk
            )

            old_status = old_obj.status
            old_paid_amount = old_obj.paid_amount



        if obj.status == "Delivered" and not obj.delivery_date:

            obj.delivery_date = timezone.now()



        super().save_model(
            request,
            obj,
            form,
            change
        )



        if obj.paid_amount > old_paid_amount:

            PaymentHistory.objects.create(

                application=obj,

                amount=(
                    obj.paid_amount -
                    old_paid_amount
                ),

                payment_mode=obj.payment_mode,

                payment_status=obj.payment_status,

                payment_reference_no=
                obj.payment_reference_no,

                receipt_no=obj.receipt_no,
            )



        if not change or old_status != obj.status:

            ApplicationStatusHistory.objects.create(

                application=obj,

                status=obj.status,

                remark=obj.remarks,

            )



    def mark_delivered_button(self,obj):

        if obj.status != "Delivered":

            return format_html(
                '<a class="button" href="mark-delivered/{}/">Delivered</a>',
                obj.id
            )

        return "Delivered"


    mark_delivered_button.short_description = "Action"



    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                'mark-delivered/<int:app_id>/',
                self.admin_site.admin_view(
                    self.mark_delivered
                ),
                name="mark_delivered"
            ),

        ]

        return custom_urls + urls



    def mark_delivered(self,request,app_id):

        application = Application.objects.get(
            id=app_id
        )

        application.status = "Delivered"
        application.delivery_date = timezone.now()

        application.save()


        ApplicationStatusHistory.objects.create(
            application=application,
            status="Delivered",
            remark=application.remarks
        )


        return redirect(
            "/admin/customers_app/application/"
        )
# =========================
# APPLICATION STATUS HISTORY
# =========================

@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'status',
        'updated_at'
    )

    search_fields = (
        'application__application_no',
        'status'
    )



# =========================
# PAYMENT HISTORY
# =========================

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

    list_filter = (
        'payment_mode',
        'payment_status',
        'created_at'
    )

    search_fields = (
        'application__application_no',
        'payment_reference_no',
        'receipt_no',
    )



# =========================
# GRIEVANCE ADMIN
# =========================

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):

    list_display = (
    'id',
    'ticket_no',
    'name',
    'mobile',
    'application',
    'category',
    'priority',
    'status',
    'attachment',
    'created_at',
)

    list_editable = (
        'status',
    )

    list_filter = (
        'status',
        'priority',
        'category'
    )

    search_fields = (
        'ticket_no',
        'name',
        'mobile'
    )



@admin.register(GrievanceHistory)
class GrievanceHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'grievance',
        'status',
        'created_at'
    )



# =========================
# ADMIN DASHBOARD
# =========================

old_index = admin.site.index


def custom_admin_index(request, extra_context=None):

    extra_context = extra_context or {}


    extra_context["total_customers"] = (
        Customer.objects.count()
    )


    extra_context["total_applications"] = (
        Application.objects.count()
    )


    extra_context["pending_count"] = (
        Application.objects.filter(
            status="Pending"
        ).count()
    )


    extra_context["submitted_count"] = (
        Application.objects.filter(
            status="Submitted"
        ).count()
    )


    extra_context["in_process_count"] = (
        Application.objects.filter(
            status="In Process"
        ).count()
    )


    extra_context["approved_count"] = (
        Application.objects.filter(
            status="Approved"
        ).count()
    )


    extra_context["rejected_count"] = (
        Application.objects.filter(
            status="Rejected"
        ).count()
    )


    extra_context["delivered_count"] = (
        Application.objects.filter(
            status="Delivered"
        ).count()
    )


    extra_context["paid_count"] = (
        Application.objects.filter(
            payment_status="Paid"
        ).count()
    )


    extra_context["unpaid_count"] = (
        Application.objects.filter(
            payment_status="Unpaid"
        ).count()
    )


    applications = Application.objects.all()


    extra_context["total_collection"] = sum(
        app.paid_amount
        for app in applications
    )


    extra_context["total_due"] = sum(
        app.due_amount
        for app in applications
    )


    extra_context["cash_collection"] = sum(
        app.paid_amount
        for app in applications
        if app.payment_mode == "Cash"
    )


    extra_context["online_collection"] = sum(
        app.paid_amount
        for app in applications
        if app.payment_mode == "Online"
    )


    extra_context["total_grievances"] = (
        Grievance.objects.count()
    )


    extra_context["grievance_pending"] = (
        Grievance.objects.filter(
            status="Pending"
        ).count()
    )


    extra_context["grievance_resolved"] = (
        Grievance.objects.filter(
            status="Resolved"
        ).count()
    )


    return old_index(
        request,
        extra_context=extra_context
    )


admin.site.index = custom_admin_index



# =========================
# DATABASE BACKUP
# =========================

def backup_database(request):

    backup_file = os.path.join(
        settings.BASE_DIR,
        "acz_full_backup.json"
    )


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


    with open(
        backup_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(data)



    return FileResponse(
        open(backup_file,"rb"),
        as_attachment=True,
        filename="acz_full_backup.json"
    )



old_get_urls = admin.site.get_urls


def custom_get_urls():

    urls = old_get_urls()


    custom_urls = [

        path(
            "backup-database/",
            admin.site.admin_view(
                backup_database
            ),
            name="backup_database"
        ),

    ]


    return custom_urls + urls



admin.site.get_urls = custom_get_urls




# =========================
# NOTICE ADMIN
# =========================

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'priority',
        'active',
        'created_at'
    )

    list_editable = (
        'active',
    )

    list_filter = (
        'priority',
        'active'
    )

    search_fields = (
        'title',
        'message'
    )

    
# =========================
# UPI PAYMENT VERIFICATION
# =========================

@admin.register(UpiPaymentSubmission)
class UpiPaymentSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "application",
        "amount",
        "utr",
        "status",
        "submitted_at",
        "reviewed_by",
        "open_payment",
    )

    list_filter = ("status", "submitted_at")

    search_fields = (
        "utr",
        "application__application_no",
        "application__customer__name",
        "application__customer__aadhaar_no",
        "application__customer__contact_no",
    )

    list_select_related = (
        "application",
        "application__customer",
        "reviewed_by",
    )

    # Payment details must be opened and reviewed individually.
    actions = None

    readonly_fields = (
        "application",
        "amount",
        "utr",
        "status",
        "reviewed_by",
        "submitted_at",
        "reviewed_at",
        "customer_details",
        "application_details",
        "payment_review_status",
    )

    fieldsets = (
        ("Customer Details", {
            "fields": (
                "customer_details",
            )
        }),
        ("Application Details", {
            "fields": (
                "application_details",
                "application",
            )
        }),
        ("Submitted Payment", {
            "fields": (
                "amount",
                "utr",
                "submitted_at",
                "status",
            )
        }),
        ("Admin Verification", {
            "fields": (
                "admin_note",
                "payment_review_status",
                "reviewed_by",
                "reviewed_at",
            )
        }),
    )

    @admin.display(description="Customer")
    def customer_name(self, obj):
        return obj.application.customer.name

    @admin.display(description="Open payment")
    def open_payment(self, obj):
        from django.urls import reverse

        url = reverse(
            "admin:customers_app_upipaymentsubmission_change",
            args=[obj.pk],
        )

        return format_html(
            '<a class="button" href="{}">View Details</a>',
            url,
        )

    @admin.display(description="Customer information")
    def customer_details(self, obj):
        customer = obj.application.customer

        return format_html(
            "<b>Name:</b> {}<br>"
            "<b>Mobile:</b> {}<br>"
            "<b>Aadhaar:</b> {}",
            customer.name or "—",
            customer.contact_no or "—",
            customer.aadhaar_no or "—",
        )

    @admin.display(description="Application information")
    def application_details(self, obj):
        application = obj.application

        return format_html(
            "<b>Application No:</b> {}<br>"
            "<b>Service:</b> {}<br>"
            "<b>Total Amount:</b> ₹{}<br>"
            "<b>Already Paid:</b> ₹{}<br>"
            "<b>Current Due:</b> ₹{}<br>"
            "<b>Payment Mode:</b> {}",
            application.application_no or "—",
            application.part,
            application.amount,
            application.paid_amount,
            application.due_amount,
            application.payment_mode or "—",
        )

    @admin.display(description="Verification status")
    def payment_review_status(self, obj):
        if obj.status == "Pending":
            return format_html(
                '<span style="color:#b45309;font-weight:bold;">{}</span>',
                "Pending verification — check UTR in your bank/UPI app",
            )

        return format_html(
            "<b>{}</b>",
            obj.status,
        )


    def get_urls(self):
        from django.urls import path

        custom_urls = [
            path(
                "<int:object_id>/clear-payment/",
                self.admin_site.admin_view(self.clear_payment),
                name="customers_app_upipaymentsubmission_clear",
            ),
        ]

        return custom_urls + super().get_urls()

    
    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        from django.urls import reverse

        if obj and obj.pk and obj.status == "Pending":
            context["clear_payment_url"] = reverse(
                "admin:customers_app_upipaymentsubmission_clear",
                args=[obj.pk],
            )

        return super().render_change_form(
            request,
            context,
            add=add,
            change=change,
            form_url=form_url,
            obj=obj,
        )

    
    def response_change(self, request, obj):
        if "_clear_payment" in request.POST:
            return self.clear_payment(request, obj.pk)

        if "_reject_payment" in request.POST:
            return self.reject_payment(request, obj.pk)

        return super().response_change(request, obj)



    
    def reject_payment(self, request, object_id):
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        from django.shortcuts import get_object_or_404
        from django.urls import reverse
        from django.utils import timezone

        submission = get_object_or_404(
            UpiPaymentSubmission,
            pk=object_id
        )

        change_url = reverse(
            "admin:customers_app_upipaymentsubmission_change",
            args=[submission.pk]
        )

        if request.method != "POST":
            return HttpResponseRedirect(change_url)

        if submission.status != "Pending":
            messages.warning(
                request,
                "This payment has already been reviewed."
            )
            return HttpResponseRedirect(change_url)

        submission.status = "Rejected"
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save(
            update_fields=["status", "reviewed_by", "reviewed_at"]
        )

        messages.warning(
            request,
            "Payment rejected. The customer can submit payment details again."
        )

        return HttpResponseRedirect(change_url)


    def clear_payment(self, request, object_id):
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        from django.shortcuts import get_object_or_404
        from django.urls import reverse
        from django.utils.http import url_has_allowed_host_and_scheme

        if request.method != "POST":
            messages.error(request, "Please use the Clear Payment button.")
            return HttpResponseRedirect(
                reverse(
                    "admin:customers_app_upipaymentsubmission_change",
                    args=[object_id],
                )
            )

        submission = get_object_or_404(
            UpiPaymentSubmission,
            pk=object_id,
        )

        change_url = reverse(
            "admin:customers_app_upipaymentsubmission_change",
            args=[object_id],
        )

        if submission.status != "Pending":
            messages.warning(request, "This payment has already been reviewed.")
            return HttpResponseRedirect(change_url)

        if not request.POST.get("confirm_clear"):
            messages.error(
                request,
                "Confirm that you have verified the UTR in your bank/UPI app.",
            )
            return HttpResponseRedirect(change_url)

        with transaction.atomic():
            submission = (
                UpiPaymentSubmission.objects
                .select_for_update()
                .get(pk=object_id)
            )

            if submission.status != "Pending":
                messages.warning(request, "This payment has already been reviewed.")
                return HttpResponseRedirect(change_url)

            application = (
                Application.objects
                .select_for_update()
                .get(pk=submission.application_id)
            )

            if (
                submission.amount <= 0
                or application.due_amount <= 0
                or submission.amount > application.due_amount
            ):
                submission.admin_note = (
                    "Approval blocked: submitted amount does not match "
                    "the current due. Please review manually."
                )
                submission.save(update_fields=["admin_note"])
                messages.error(
                    request,
                    "Payment not cleared. Submitted amount does not match the current due.",
                )
                return HttpResponseRedirect(change_url)

            application.paid_amount += submission.amount
            application.payment_mode = "Online"
            application.save()

            PaymentHistory.objects.create(
                application=application,
                amount=submission.amount,
                payment_mode="Online",
                payment_status="Paid",
                payment_reference_no=submission.utr,
                receipt_no=application.receipt_no,
            )

            submission.status = "Approved"
            submission.reviewed_by = request.user
            submission.reviewed_at = timezone.now()
            submission.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                ]
            )

        messages.success(
            request,
            "Payment cleared and recorded successfully.",
        )
        return HttpResponseRedirect(change_url)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
