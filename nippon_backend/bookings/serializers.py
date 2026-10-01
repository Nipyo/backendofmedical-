from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """camelCase JSON (matches the Next.js `Booking` type) <-> snake_case model."""

    fullName = serializers.CharField(source="full_name", max_length=255)
    email = serializers.EmailField()
    dateOfBirth = serializers.DateField(source="date_of_birth")
    appointmentDate = serializers.DateTimeField(source="appointment_date")
    message = serializers.CharField(required=False, allow_blank=True)
    phoneNumber = serializers.CharField(source="phone_number", max_length=32)
    passportNumber = serializers.CharField(source="passport_number", max_length=32)
    passportIssueDate = serializers.DateField(source="passport_issue_date")
    passportExpiryDate = serializers.DateField(source="passport_expiry_date")
    gender = serializers.CharField(max_length=20)
    age = serializers.IntegerField(required=False, allow_null=True, min_value=0, max_value=130)
    status = serializers.ChoiceField(choices=Booking.Status.choices, required=False)
    doctor = serializers.CharField(required=False, allow_blank=True, max_length=255)
    department = serializers.CharField(required=False, allow_blank=True, max_length=255)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "fullName", "email", "dateOfBirth", "appointmentDate", "message",
            "phoneNumber", "passportNumber", "passportIssueDate", "passportExpiryDate",
            "gender", "age", "status", "createdAt", "doctor", "department",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        issue = attrs.get("passport_issue_date")
        expiry = attrs.get("passport_expiry_date")
        if issue and expiry and expiry <= issue:
            raise serializers.ValidationError(
                {"passportExpiryDate": "Expiry date must be after the issue date."}
            )
        return attrs
