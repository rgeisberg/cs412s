from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.
class show_all_profiles(ListView):
    """Define a view class to show all profiles"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class profile_detail_view(DetailView):
    """Define a view class to show all profiles"""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
