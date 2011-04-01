from django.db import models
from django.contrib.auth.models import User

class CandidateInfo(models.Model):
  content = models.TextField()
  picture = models.CharField(max_length=1000)

#TODO: Rename to UserInfo
class UserProfile(models.Model):
  user       = models.OneToOneField(User)
  is_anon    = models.BooleanField() #anon user?
  info       = models.ForeignKey(CandidateInfo, null=True, blank=True)

  is_special          = models.BooleanField() #a candidate?
  challenges          = models.IntegerField()
  challenges_answered = models.IntegerField()


  def __unicode__(self):
    if self.is_special:
      return "%s is special." % (self.user.username)
    return "%s is not special." % (self.user.username)