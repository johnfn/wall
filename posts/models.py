from django.db import models
from wall.users.models import UserExtra

class Post(models.Model):
  title    = models.CharField(max_length=1000)
  content  = models.TextField()
  #creator = models.ForeignKey(User)
  creator  = models.CharField(max_length=100)
  creators = models.ForeignKey(UserExtra)
  #date    = models.DateTimeField('date published')

  #num_likes #LOL

  def __unicode__(self):
    return self.content

class Comment(models.Model):
  parent   = models.ForeignKey(Post)
  content  = models.TextField()
  creator  = models.CharField(max_length=100)
  creators = models.ForeignKey(UserExtra)


  def __unicode__(self):
    return self.content