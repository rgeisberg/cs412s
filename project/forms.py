# File: forms.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: forms file for recipe

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class CustomUserCreationForm(UserCreationForm):
    """create user"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CommentReviewForm(forms.ModelForm):
    """leave comment"""
    class Meta:
        model = CommentReview
        fields = ['rating', 'comment']

class RecipeURLForm(forms.Form):
    """create a recipe from url"""
    url = forms.URLField(label='Recipe URL', help_text='Enter a valid recipe URL.')

class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'image', 'steps']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }
