from django.contrib import admin
from passport.residence_permit.models import ResidencePermit

@admin.register(ResidencePermit)
class ResidencePermitAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "permit_number",
        "document",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "permit_number",
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