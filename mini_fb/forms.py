# File: forms.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: forms file for mini_fb

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """a form to collect inputs to create a new Profile"""
    
    class Meta:
        '''associate this form with the profile model; select fields.'''
        model = Profile
        fields = [ 'firstName', 'lastName', 'city', 'email', 'profileImageUrl' ]  # which fields from model should we use


class CreateStatusMessageForm(forms.ModelForm):
    """a form for the user to create a status message"""
    class Meta:
        '''associate this form with the StatusMessage model; select fields.'''
        model = StatusMessage
        fields = ['message']  # which fields from model should we use

class UpdateProfileForm(forms.ModelForm):
    """form to update an exsisting profile"""
    class Meta:
        """associate this form with the profile model"""
        model = Profile
        fields = ['city', 'email' , 'profileImageUrl' ]




