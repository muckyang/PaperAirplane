from django.urls import path, include
from rest_framework import routers
from .views import TempDelectViewSet, TempCreateViewSet,TempReadViewSet
from route import views
from django.conf.urls import url

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'tempDelete', views.TempDelectViewSet, basename="tempD")
router.register(r'tempCreate', views.TempCreateViewSet, basename="tempC")
router.register(r'tempRead', views.TempReadViewSet, basename="tempR")

urlpatterns = router.urls