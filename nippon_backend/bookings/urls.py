from rest_framework.routers import SimpleRouter

from .views import BookingViewSet

router = SimpleRouter(trailing_slash=False)
router.register("Booking", BookingViewSet, basename="booking")

urlpatterns = router.urls
