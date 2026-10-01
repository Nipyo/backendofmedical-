from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

PAYLOAD = {
    "fullName": "Test Patient",
    "email": "patient@example.com",
    "dateOfBirth": "1990-05-01",
    "appointmentDate": "2026-11-10T10:30:00+05:45",
    "message": "First visit",
    "phoneNumber": "+977 9800000000",
    "passportNumber": "P1234567",
    "passportIssueDate": "2022-01-01",
    "passportExpiryDate": "2032-01-01",
    "gender": "male",
    "age": 36,
    "doctor": "Dr. Tanaka",
    "department": "Cardiology",
    "status": "confirmed",
}


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    BOOKING_NOTIFY_EMAILS=["client@example.com"],
    BOOKING_ADMIN_API_PUBLIC=False,
)
class BookingApiTests(APITestCase):
    def test_public_create_sends_email_and_forces_pending(self):
        r = self.client.post("/api/Booking", PAYLOAD, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(r.data["status"], "pending")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["client@example.com"])
        self.assertIn("Test Patient", mail.outbox[0].body)

    def test_anonymous_cannot_read(self):
        self.client.post("/api/Booking", PAYLOAD, format="json")
        self.assertIn(self.client.get("/api/Booking/1").status_code, (401, 403))

    def test_bad_passport_dates_rejected(self):
        bad = {**PAYLOAD, "passportExpiryDate": "2021-01-01"}
        r = self.client.post("/api/Booking", bad, format="json")
        self.assertEqual(r.status_code, 400)
