from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Article, Publisher
from .serializers import ArticleSerializer, PublisherSerializer

class IsReaderOrAbove(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsReaderOrAbove]

    def get_queryset(self):
        user = self.request.user
        qs = Article.objects.filter(approved=True)

        if getattr(user, "role", None) == "reader":
            pubs = user.subscribed_publishers.all()
            journos = user.subscribed_journalists.all()
            return qs.filter(Q(publisher__in=pubs) | Q(author__in=journos)).distinct()

        return qs

class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsReaderOrAbove]