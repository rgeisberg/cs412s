# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: url file for mini_fb
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ShowAllProfilesView, ShowProfile, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView, ShowNewsFeedView,LogoutConfirmationView

urlpatterns = [
    path('',ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfile.as_view(), name="profile"),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions' ),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'), 
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout' ),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),

]