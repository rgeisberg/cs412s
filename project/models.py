# File: model.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: model file for recipe

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    """profile using django built in user that has username, email, password, date_joined"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recipe_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    
    
class Recipe(models.Model):
    RECIPE_TYPE_CHOICES = [
        ('Created', 'Created'),
        ('Scraped', 'Scraped'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.TextField()
    description = models.TextField()
    cuisine_type = models.TextField(null=True, blank=True)
    cooking_time = models.IntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    steps = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # Track source (optional for scraped)
    recipe_type = models.CharField(max_length=10, choices=RECIPE_TYPE_CHOICES)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    source_url = models.TextField(blank=True, null=True)
    source_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.recipe_type} Recipe: {self.title}'
    

class Ingredient(models.Model):
    '''class for ingredient objects'''
    ingredient_name = models.TextField()
    quantity = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) ## do i want the ingredients to delete on cascade?? do i care about duplicates

    def __str__(self):
            return f'{self.ingredient_name} Recipe: {self.recipe}'
    
class SavedRecipie(models.Model):
    """class to represent relationship between users and recipies"""
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at_time = models.DateTimeField()


class CommentReview(models.Model):
    """comment on recipies"""
    RATING = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating= models.CharField(max_length=10, choices=RATING, blank=True)
    comment = models.TextField()
    date_posted = models.DateTimeField()
    



