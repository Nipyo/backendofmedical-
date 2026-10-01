from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.throttling import AnonRateThrottle

from .emails import send_booking_notification
from .models import Booking
from .serializers import BookingSerializer


class BookingPermission(permissions.BasePermission):
    """Anyone can SUBMIT the form. Reading/editing/deleting needs a login token."""

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if settings.BOOKING_ADMIN_API_PUBLIC:  # dev only
            return True
        return bool(request.user and request.user.is_authenticated)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [BookingPermission]

    def get_throttles(self):
        return [AnonRateThrottle()] if self.action == "create" else []

    def perform_create(self, serializer):
        extra = {}
        user = self.request.user
        if not (user and user.is_authenticated):
            extra["status"] = Booking.Status.PENDING  # public users can't self-confirm
        booking = serializer.save(**extra)
        send_booking_notification(booking)  # booking is saved even if email fails
