from django.contrib import admin
from passport.vehicle_inspection_certificate.models import VehicleInspectionCertificate

@admin.register(VehicleInspectionCertificate)
class VehicleInspectionCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "certificate_number",
        "document",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "certificate_number",
        "user_id__email",
        "user_id__username",
        "first_name",
        "last_name",
    )

    list_filter = (
        "issue_country",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )