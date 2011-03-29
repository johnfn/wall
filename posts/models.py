from django.db import models

class Post(models.Model):
  title   = models.CharField(max_length=1000)
  content = models.TextField()
  #creator = models.ForeignKey(User)
  creator = models.CharField(max_length=100)
  #date    = models.DateTimeField('date published')

  #num_likes #LOL

  def __unicode__(self):
    return self.content

class Comment(models.Model):
  parent  = models.ForeignKey(Post)
  content = models.TextField()
  creator = models.CharField(max_length=100)

  def __unicode__(self):
    return self.content