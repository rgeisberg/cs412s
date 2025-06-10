#blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
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
    ## auth paths
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout' ),
    path('register/', UserRegistrationView.as_view(), name='register'),


    
]