# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: url file for mini_fb
from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('',ShowAllProfilesView.as_view(), name='show_all_profiles'),
]