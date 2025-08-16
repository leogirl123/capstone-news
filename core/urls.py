from django.urls import path
from . import views

urlpatterns = [
    path("", views.public_article_list, name="home"),
    path("articles/<int:pk>/", views.public_article_detail, name="article_detail"),
    path("dashboard/editor/", views.editor_dashboard, name="editor_dashboard"),
    path("articles/<int:pk>/approve/", views.approve_article, name="approve_article"),
]