# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: urls file for voter analytics\

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]