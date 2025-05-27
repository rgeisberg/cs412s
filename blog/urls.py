#blog/urls.py
from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleVIew
urlpatterns = [
    path('',RandomArticleVIew.as_view(), name='random'),
    path('show_all',ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticleView.as_view(), name="article"),

]