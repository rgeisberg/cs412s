# File: admin.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: admin file for voter analytics
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Voter)
