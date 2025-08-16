from rest_framework import serializers
from .models import Article, Publisher, User, Newsletter

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "description"]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ["id", "title", "body", "author", "publisher", "approved", "approved_at", "created_at"]

class NewsletterSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    class Meta:
        model = Newsletter
        fields = ["id", "title", "content", "author", "publisher", "created_at"]