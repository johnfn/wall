from django.db import models
from django.contrib.auth.models import User

class CandidateInfo(models.Model):
  content = models.TextField()
  picture = models.CharField(max_length=1000)

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
  info       = models.ForeignKey(CandidateInfo, null=True, blank=True)
  supports   = models.ForeignKey(User, null=True, blank=True, related_name="support")
  
  is_special          = models.BooleanField() #a candidate?
  challenges          = models.IntegerField()
  challenges_answered = models.IntegerField()
  supporters          = models.IntegerField()
  
  objects = UserProfileManager()
  
  def __unicode__(self):
    if self.is_special:
      return "%s is special." % (self.user.username)
    return "%s is not special." % (self.user.username)