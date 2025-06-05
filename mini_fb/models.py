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
    
    def get_friends(self):
        '''accessor method to get all friend '''
        friends = []
        # Friends where this profile is profile1
        friendships_as_profile1 = Friend.objects.filter(profile1=self)
        for friendship in friendships_as_profile1:
                friends.append(friendship.profile2)

        # Friends where this profile is profile2
        friendships_as_profile2 = Friend.objects.filter(profile2=self)
        for friendship in friendships_as_profile2:
                friends.append(friendship.profile1)
        return friends
    
    def add_friend(self, other):
        """Add a Friend relation for the two Profiles: self and other."""
        if self == other:
                print("Cannot self-friend")
                return

        # Check for existing friendship in either direction
        existing_friendship1 = Friend.objects.filter(profile1=self, profile2=other).exists()
        existing_friendship2 = Friend.objects.filter(profile1=other, profile2=self).exists()

        if not existing_friendship1 and not existing_friendship2:
                # Create and save the new Friend relationship
                new_friendship = Friend(profile1=self, profile2=other)
                new_friendship.save()

    def get_friend_suggestions(self):
        """Return Profiles that are not already friends and not self."""
        current_friends = self.get_friends()
        current_friend_ids = [p.pk for p in current_friends]
        all_other_profiles = Profile.objects.exclude(pk=self.pk)
        suggestions = all_other_profiles.exclude(pk__in=current_friend_ids)
        return suggestions     
         
          


class StatusMessage(models.Model):
    """Encapsulate the data of a status message """
    #define the data attributes
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
            """return a string representation of this model"""
            return f'{self.message} made at {self.timestamp} by {self.profile}'
    
    def get_images(self):
        """acessor method for all images """
        images = StatusImage.objects.filter(status_message=self)
        return images


    
class Image(models.Model):
      """Encapsulate the data of an  image """
      profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
      image_file = models.ImageField(blank=True)
      timestamp = models.DateTimeField(auto_now=True)
      caption = models.TextField(blank=True)

      def __str__(self):
        return f"Image for {self.profile.firstName}"

      # make the form?? with meta data if not asked to later

class StatusImage(models.Model):
      """Encapsulate the relationship between images and status messages"""
      image = models.ForeignKey("Image", on_delete=models.CASCADE)
      status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

      def __str__(self):
        return f"image plus {self.status_message}"



class Friend(models.Model):
     """Encapsulate the friend relationship as a model"""
     profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
     profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
     timestamp = models.DateTimeField(auto_now=True)
     
     def __str__(self):
        return f"{self.profile1} & {self.profile2}"


