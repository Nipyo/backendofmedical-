from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone_number", "appointment_date",
                    "doctor", "department", "status", "created_at")
    list_filter = ("status", "department", "doctor")
    search_fields = ("full_name", "email", "phone_number", "passport_number")
    ordering = ("-created_at",)
