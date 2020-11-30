from django.urls import path, include
from .views import CommentViewSet, CreateAPI, CommentUpdateAPI, CommentDeleteAPI
from rest_framework import routers
from .views import CommentViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'commentread', CommentViewSet)


urlpatterns = [
    path("create/", CreateAPI.as_view()),
    path("update/", CommentUpdateAPI.as_view()),
    path("delete/<int:pk>", CommentDeleteAPI.as_view()),
]
urlpatterns += router.urls