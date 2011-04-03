from django.db import models
from django.contrib.auth.models import User

class UserProfileManager(models.Manager):    
  def create_profile(self, user, is_anon=False, is_special=False,\
        challenges=0, challenges_answered=0, supporters=0):
    # Create a base user profile. Values are simply initiated because the database will not accept
    # any null values. These will all be changed when the user sets up a new profile anyway.
    profile = self.model(user=user, is_anon=is_anon, is_special=is_special, challenges=challenges,\
        challenges_answered=challenges_answered, supporters=supporters)
    profile.save()
    return profile

class UserProfile(models.Model):
  user       = models.OneToOneField(User)
  is_anon    = models.BooleanField() #anon user?
  supports0  = models.ForeignKey(User, null=True, blank=True, related_name="support0")
  supports1  = models.ForeignKey(User, null=True, blank=True, related_name="support1")
  supports2  = models.ForeignKey(User, null=True, blank=True, related_name="support2")
  supports3  = models.ForeignKey(User, null=True, blank=True, related_name="support3")
  
  is_special          = models.BooleanField() #a candidate?
  which_race          = models.IntegerField()
  challenges          = models.IntegerField()
  challenges_answered = models.IntegerField()
  supporters          = models.IntegerField()
  info                = models.TextField(null=True, blank=True)
  
  objects = UserProfileManager()
  
  def __unicode__(self):
    if self.is_special:
      return "%s is special." % (self.user.username)
    return "%s is not special." % (self.user.username)
