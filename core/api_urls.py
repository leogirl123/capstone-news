from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, PublisherViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="articles")
router.register(r"publishers", PublisherViewSet, basename="publishers")

urlpatterns = [
    path("", include(router.urls)),
]