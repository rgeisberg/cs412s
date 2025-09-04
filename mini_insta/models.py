from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField()
    bio_text = models.TextField()
    join_date = models.DateField()
