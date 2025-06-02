#blog/urls.py
from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleVIew, CreateCommentView, CreateArticleView, UpdateArticleView, DeleteCommentView
urlpatterns = [
    # map the URL (empty string) to the view
	## new view for 'random', refactor 'show_all'
    path('', RandomArticleVIew.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
     path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'), 
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
   
    
]