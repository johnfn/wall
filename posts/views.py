from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from wall.posts.models import Post, Comment
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
import datetime


def home(request):
  return render_to_response( "index.html"
                           , { "posts" : Post.objects.all() 
                             }
                           , context_instance=RequestContext(request)
                           )

def post_post(request):
  content  = request.POST["content"]
  username = request.POST["name"]

  new_post = Post(content=content, creator=username)
  new_post.save()

  return HttpResponseRedirect("/")

def post_comment(request, id):
  content = request.POST['content']
  username = request.POST['name']

  new_comment = Comment(content=content, creator=username, parent=Post.objects.get(id=int(id)))
  new_comment.save()

  return HttpResponseRedirect("/")