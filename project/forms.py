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
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CommentReviewForm(forms.ModelForm):
    class Meta:
        model = CommentReview
        fields = ['rating', 'comment']