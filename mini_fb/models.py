# File: model.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: model file for mini_fb
from django.db import models

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


