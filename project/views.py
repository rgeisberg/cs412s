from django.shortcuts import render
# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for recipe

from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse 
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowAllRecipes(ListView):
    """view to show all recipes"""
    model = Recipe
    template_name = 'project/show_all_recipes.html'  # customize as needed
    context_object_name = 'recipes'
    ordering = ['-date_added']  # newest first

class RecipeDetailView(DetailView):
    """view each recipe in detail"""
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'


class CustomLoginView(LoginView):
    template_name = 'project/login.html'

    def get_success_url(self):
        return  '/project/recipes/'
    

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "project/signup_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = CustomUserCreationForm()
        return context

    def form_valid(self, form):
        user_form = CustomUserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, user_creation_form=user_form)
            )


    def get_success_url(self):
        return '/project/recipes/'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'project/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.recipe_profile  # your related_name
        return context