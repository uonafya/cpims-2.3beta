"""API urls."""
from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, OrgUnitsViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'org_units', OrgUnitsViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]
