from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path, include
from .views import TitleCheckAPI


router = DefaultRouter(trailing_slash=False)
router.register(r"stores", views.StoreViewSet, basename="stores")
router.register(r"reviews", views.ReviewViewSet, basename="reviews")
router.register(r"tourspots", views.TourSpotViewSet, basename="tourspots")
router.register(r"courses",views.CourseViewSet, basename="courses")
router.register(r"recommendStores",views.RecommendStoreSet, basename="recommendStores")
router.register(r"recommendTourSpot",views.RecommendTourSpotSet, basename="recommendTourSpot")
router.register(r"recommandspots",views.RecommandViewSet, basename="recommandspots")
router.register(r"overviews",views.OverviewViewSet, basename="overviews")
router.register(r"topFiveStores",views.TopFiveViewSet, basename="topfivestores")

router.register(r'routeCreate', views.RouteCreateViewSet, basename="routeC")
router.register(r'routeRankRead', views.RouteRankReadViewSet, basename="routeRankR")
router.register(r'routeRead', views.RouteReadViewSet, basename="routeR")
router.register(r'routeDetailRead', views.RouteDetailReadViewSet, basename="routeDetailR")
# router.register(r'routeDelete', views.RouteDeleteViewSet, basename="routeD")
router.register(r"routeClickUpdate",views.RouteClickUpdateViewSet, basename="routeClickUpdate")
router.register(r"userrecommad",views.UserRecommandViewSet, basename="userrecommad")
router.register(r"recommendAuto",views.RecommandAutoViewSet, basename="recommendAuto")
urlpatterns = [
    path("titlecheck", TitleCheckAPI.as_view()),
]
urlpatterns += router.urls
