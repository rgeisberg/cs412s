#file: urls.py

from django.urls import path
from django.conf import settings
from . import views 

#URL patterns for quotes app
urlpatterns = [
    path(r'', views.quote, name='home_page'),
    path(r'quote/', views.quote, name='quote_page'),
    path(r'show_all/', views.show_all, name='show_all_page'),
    path(r'about/', views.about, name='about_page'),

]