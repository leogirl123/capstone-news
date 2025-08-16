from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mass_mail
from django.db import transaction
from django.apps import apps

from .models import User, Article, Newsletter


def ensure_perm(codename: str, name: str, ct: ContentType) -> Permission:
    """Get or create a permission safely."""
    perm, _ = Permission.objects.get_or_create(
        codename=codename,
        content_type=ct,
        defaults={"name": name},
    )
    return perm


@receiver(post_migrate)
def create_groups_permissions(sender, **kwargs):
    """
    Create/refresh groups & permissions after migrations.
    Only run for our 'core' app.
    """
    if getattr(sender, "label", None) != "core":
        return

    ArticleModel = apps.get_model("core", "Article")
    NewsletterModel = apps.get_model("core", "Newsletter")

    # Groups
    reader, _ = Group.objects.get_or_create(name="Reader")
    editor, _ = Group.objects.get_or_create(name="Editor")
    journalist, _ = Group.objects.get_or_create(name="Journalist")

    # Content types
    art_ct = ContentType.objects.get_for_model(ArticleModel)
    news_ct = ContentType.objects.get_for_model(NewsletterModel)

    # Ensure built-in + custom perms exist
    add_article    = ensure_perm("add_article",    "Can add article",    art_ct)
    view_article   = ensure_perm("view_article",   "Can view article",   art_ct)
    change_article = ensure_perm("change_article", "Can change article", art_ct)
    delete_article = ensure_perm("delete_article", "Can delete article", art_ct)
    approve_article = ensure_perm("can_approve_article", "Can approve article", art_ct)

    add_news    = ensure_perm("add_newsletter",    "Can add newsletter",    news_ct)
    view_news   = ensure_perm("view_newsletter",   "Can view newsletter",   news_ct)
    change_news = ensure_perm("change_newsletter", "Can change newsletter", news_ct)
    delete_news = ensure_perm("delete_newsletter", "Can delete newsletter", news_ct)

    # Assign
    reader.permissions.set([view_article, view_news])

    editor.permissions.set([
        view_article, change_article, delete_article,
        view_news, change_news, delete_news,
        approve_article,
    ])

    journalist.permissions.set([
        add_article, view_article, change_article, delete_article,
        add_news, view_news, change_news, delete_news,
    ])


@receiver(post_save, sender=User)
def assign_group_on_role(sender, instance: User, created, **kwargs):
    role_to_group = {"reader": "Reader", "editor": "Editor", "journalist": "Journalist"}
    group_name = role_to_group.get(instance.role)
    if not group_name:
        return
    instance.groups.clear()
    group = Group.objects.get(name=group_name)
    instance.groups.add(group)

    # If journalist, clear reader subscription fields
    if instance.role == "journalist":
        instance.subscribed_publishers.clear()
        instance.subscribed_journalists.clear()


@receiver(post_save, sender=Article)
def on_article_approved(sender, instance: Article, created, **kwargs):
    """
    When an article is approved, email subscribers of the publisher and
    followers (reader-subscribers) of the author.
    """
    if not instance.approved or not instance.approved_at or not instance.approved_by:
        return

    emails = set()
    if instance.publisher:
        emails.update(u.email for u in instance.publisher.subscribed_readers.all() if u.email)
    emails.update(u.email for u in instance.author.followers.all() if u.email)

    if emails:
        subject = f"New article: {instance.title}"
        body = instance.body[:500] + ("..." if len(instance.body) > 500 else "")
        datatuple = tuple((subject, body, None, [e]) for e in emails)
        transaction.on_commit(lambda: send_mass_mail(datatuple, fail_silently=True))