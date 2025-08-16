from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import Article

def public_article_list(request):
    articles = Article.objects.filter(approved=True).order_by("-approved_at")
    return render(request, "core/public_article_list.html", {"articles": articles})

def public_article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, approved=True)
    return render(request, "core/public_article_detail.html", {"article": article})

@login_required
@permission_required("core.can_approve_article", raise_exception=True)
def editor_dashboard(request):
    pending = Article.objects.filter(approved=False).order_by("-created_at")
    return render(request, "core/editor_dashboard.html", {"pending": pending})

@login_required
@permission_required("core.can_approve_article", raise_exception=True)
def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.approved = True
    article.approved_at = timezone.now()
    article.approved_by = request.user
    article.save()  # triggers signal -> emails
    return redirect("editor_dashboard")
