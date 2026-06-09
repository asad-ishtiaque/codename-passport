from django.contrib import admin

from passport.driving_license.models import DrivingLicense



@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "license_number",
        "document",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "license_number",
        "user_id__email",
        "user_id__username",
    )

    list_filter = (
        "issue_date",
        "expiry_date",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )