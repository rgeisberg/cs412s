from django.shortcuts import render
# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for recipe

from django.views.generic import *
from .models import *
from django.urls import reverse 

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





