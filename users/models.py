from django.db import models
from django.contrib.auth.models import User


#TODO: Rename to UserInfo
class UserExtra(models.Model):
  user       = models.ForeignKey(User)
  is_special = models.BooleanField() #a candidate?
  is_anon    = models.BooleanField() #anon user?

  def __unicode__(self):
    if self.is_special:
      return "%s is special." % (self.user.username)
    else:
      return "%s is not special." % (self.user.username)