import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_booking_notification(booking) -> bool:
    """
    Send:
    1. A booking notification to the medical office.
    2. A confirmation email to the customer.

    Email failures do not prevent the booking from being saved.
    """

    appt = timezone.localtime(booking.appointment_date)

    # =====================================================
    # 1. EMAIL TO MEDICAL OFFICE
    # =====================================================

    admin_recipients = settings.BOOKING_NOTIFY_EMAILS

    if admin_recipients:
        admin_subject = (
            f"New booking #{booking.pk} - {booking.full_name}"
        )

        admin_body = f"""A new booking was submitted.

APPOINTMENT
  Booking ID:   {booking.pk}
  Date & time:  {appt:%A, %d %B %Y, %I:%M %p}
  Doctor:       {booking.doctor or '-'}
  Department:   {booking.department or '-'}
  Status:       {booking.get_status_display()}
  Message:      {booking.message or '-'}

PATIENT
  Full name:    {booking.full_name}
  Email:        {booking.email}
  Phone:        {booking.phone_number}
  Date of birth: {booking.date_of_birth}
  Gender:       {booking.gender}
  Age:          {booking.age if booking.age is not None else '-'}

PASSPORT
  Number:       {booking.passport_number}
  Issue date:   {booking.passport_issue_date}
  Expiry date:  {booking.passport_expiry_date}

Submitted at:
  {timezone.localtime(booking.created_at):%d %B %Y, %I:%M %p}

Reply to this email to answer the patient directly.
"""

        try:
            EmailMessage(
                subject=admin_subject,
                body=admin_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_recipients,
                reply_to=[booking.email],
            ).send(fail_silently=False)

            logger.info(
                "Booking %s notification sent to %s",
                booking.pk,
                admin_recipients,
            )

        except Exception:
            logger.exception(
                "Booking %s office notification failed",
                booking.pk,
            )

    # =====================================================
    # 2. EMAIL TO CUSTOMER
    # =====================================================

    if booking.email:
        customer_subject = (
            f"Nippon Medical - Booking Received #{booking.pk}"
        )

        customer_body = f"""Dear {booking.full_name},

Thank you for contacting Nippon Medical.

We have successfully received your appointment request.

BOOKING DETAILS
----------------
Booking ID:  {booking.pk}
Appointment: {appt:%A, %d %B %Y, %I:%M %p}
Doctor:      {booking.doctor or '-'}
Department:  {booking.department or '-'}

Status:      {booking.get_status_display()}

Your appointment request is currently being reviewed by our team.

We will contact you regarding the appointment and next steps.

Thank you,
Nippon Medical

This is an automated confirmation email.
"""

        try:
            EmailMessage(
                subject=customer_subject,
                body=customer_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[booking.email],
            ).send(fail_silently=False)

            logger.info(
                "Booking %s confirmation sent to customer %s",
                booking.pk,
                booking.email,
            )

        except Exception:
            logger.exception(
                "Booking %s customer email failed",
                booking.pk,
            )

    return True
