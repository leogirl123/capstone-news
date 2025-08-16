from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="publishers_as_editor", blank=True
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="publishers_as_journalist", blank=True
    )
    def __str__(self): return self.name

class User(AbstractUser):
    class Roles(models.TextChoices):
        READER = "reader", "Reader"
        EDITOR = "editor", "Editor"
        JOURNALIST = "journalist", "Journalist"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.READER)

    # Reader fields
    subscribed_publishers = models.ManyToManyField(
        Publisher, related_name="subscribed_readers", blank=True
    )
    subscribed_journalists = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    # Journalist “independent” content is inferred by Article/Newsletter with publisher=None
    @property
    def independent_articles(self):
        return Article.objects.filter(author=self, publisher__isnull=True)

    @property
    def independent_newsletters(self):
        return Newsletter.objects.filter(author=self, publisher__isnull=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # group assignment handled in signals

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles")
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_articles"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [("can_approve_article", "Can approve article")]

    def __str__(self): return self.title

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="newsletters")
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name="newsletters")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title
