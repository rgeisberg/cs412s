#blogs/views.py
#views for the blog application
from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Article 
import random 

# Create your views here.
class ShowAllView(ListView):
    """Define a view class to show all blog Articles."""
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class ArticleView(DetailView):
    """Defind a view class to show one article"""
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class RandomArticleVIew(DetailView):
    """Display a single article"""
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    #methods
    def get_object(self):
        """return one random article obj"""
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


