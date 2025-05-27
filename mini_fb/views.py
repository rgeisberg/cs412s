# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for mini_fb
from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic import ListView, DetailView 
from .models import Profile

# Create your views here.

class ShowAllProfilesView(ListView):
    """Define a view class to show all profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


