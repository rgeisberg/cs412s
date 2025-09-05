from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('', show_all_profiles.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', profile_detail_view.as_view(), name="profile")
]