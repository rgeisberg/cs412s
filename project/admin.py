# File: admin.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: admin file for recipe
from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(SavedRecipie)
admin.site.register(CommentReview)
