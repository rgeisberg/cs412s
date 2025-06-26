# File: urls.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: url file for recipe

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('recipes/', ShowAllRecipes.as_view(), name='show_all_recipes'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_recipes'), name='logout'),
    path('signup/', CreateProfileView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('recipes/<int:pk>/save/', SaveRecipeView.as_view(), name='save_recipe'),
    path('submit_recipe/', SubmitRecipeURLView.as_view(), name='submit_recipe'),
    path('submit_manual_recipe/', CreateRecipeView.as_view(), name='submit_manual_recipe'),

]