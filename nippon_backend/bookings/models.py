from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date_of_birth = models.DateField()
    appointment_date = models.DateTimeField()
    message = models.TextField(blank=True, default="")
    phone_number = models.CharField(max_length=32)
    passport_number = models.CharField(max_length=32)
    passport_issue_date = models.DateField()
    passport_expiry_date = models.DateField()
    gender = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    doctor = models.CharField(max_length=255, blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.full_name} ({self.appointment_date:%Y-%m-%d})"
