# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for mini_fb
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView 
from .models import Profile
from .forms import CreateProfileForm

# Create your views here.

class ShowAllProfilesView(ListView):
    """Define a view class to show all profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfile(DetailView):
    """Defind a view class to show one profile"""
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    """Define a view class to create profiles"""
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    context_object_name='form'




