# File: model.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: model file for mini_fb
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """Encapsulate the data of a Profile"""
    #define the data attributes
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    profileImageUrl = models.URLField(blank=True)
   # models.DateTimeField(auto_now=True)

    def __str__(self):
            """return a string representation of this model"""
            return f'{self.firstName} {self.lastName}'
    
    def get_status_messages(self):
          """return all status messages for a particular user"""
          status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
          return status_messages
    def get_absolute_url(self):
        """display new profile"""
        return reverse('profile', kwargs={'pk':self.pk})
          


class StatusMessage(models.Model):
    """Encapsulate the data of a status message """
    #define the data attributes
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
            """return a string representation of this model"""
            return f'{self.message} made at {self.timestamp} by {self.profile}'
    


