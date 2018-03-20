from rest_framework import routers

from .views import TourViewSet

router = routers.DefaultRouter()

router.register(r'tours', TourViewSet)
