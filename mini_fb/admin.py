# File: admin.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: admin file for mini_fb
from django.contrib import admin
from .models import Profile, StatusMessage, Image, StatusImage

# Register your models here.

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)        
admin.site.register(StatusImage)
