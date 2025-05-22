# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: urls file for restaurants

from django.urls import path
from django.conf import settings
from . import views 

#URL patterns for quotes app

urlpatterns = [
    path(r'main/', views.main, name='main_page'),
    path(r'order/', views.order, name='order_page'),
    path(r'confirmation/', views.confirmation, name='confirmation_page'),

]