from django.urls import path, include
from rest_framework import routers
from .views import CustomViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'custom', CustomViewSet)

urlpatterns = router.urls