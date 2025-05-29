# File: forms.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: forms file for mini_fb

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """a form to collect inputs to create a new Profile"""
    
    class Meta:
        '''associate this form with the StatusMessage model; select fields.'''
        model = Profile
        fields = [ 'firstName', 'lastName', 'city', 'email', 'profileImageUrl' ]  # which fields from model should we use



