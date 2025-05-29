# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: url file for mini_fb
from django.urls import path
from .views import ShowAllProfilesView, ShowProfile, CreateProfileView

urlpatterns = [
    path('',ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfile.as_view(), name="profile"),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
]