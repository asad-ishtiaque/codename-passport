from django.contrib import admin
from passport.passport.models import Passport

@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "passport_number",
        "document",
        "nationality",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "passport_number",
        "user_id__email",
        "user_id__username",
        "first_name",
        "last_name",
    )

    list_filter = (
        "nationality",
        "issue_country",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )