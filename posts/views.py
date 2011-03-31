from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from wall.posts.models import Post, Comment
from wall.users.models import UserExtra
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
import datetime


def home(request):
  user_info = get_user_info(request.user.username, request.user.is_authenticated())

  users = User.objects.all()
  users = [user for user in users if UserExtra.objects.get(user=user).is_special]

  return render_to_response( "index.html"
                           , { "posts"      : Post.objects.all()
                             , "loggedin"   : request.user.is_authenticated()
                             , "user"       : request.user
                             , "user_info"  : user_info
                             , "candidates" : users
                             }
                           , context_instance=RequestContext(request)
                           )

def get_user_info(username, authenticated):
  creator_info = None

  if authenticated:
    creator_info = UserExtra.objects.get(user=User.objects.get(username=username))
  else:
    creator_info = get_anon_user_info()

  return creator_info

def get_anon_user_info():
  info = None
  #Create only if necessary
  try:
    info = UserExtra.objects.get(is_anon=True)
  except:
    info = UserExtra(is_special=False, is_anon=True)
  
  return info

def post_post(request):
  content         = request.POST["content"]
  username        = request.POST["name"]
  creator_info    = get_user_info(username, request.user.is_authenticated())
  is_challenge    = ("challenge" in request.POST)
  challenged_user = None

  if is_challenge:
    try:
      challenged_user = User.objects.get(username=request.POST["challenged_user"])
    except:
      #TODO: Make graceful!
      return HttpResponse("Couldn't find that user!")
  
  new_post = Post( content         = content
                 , creator         = username
                 , creators        = creator_info

                 #Challenge stuff
                 , challenge       = is_challenge
                 , challenged_user = challenged_user
                 )
  new_post.save()

  return HttpResponseRedirect("/")

def post_comment(request, id):
  content = request.POST["content"]
  username = request.POST["name"]
  creator_info = get_user_info(username, request.user.is_authenticated())

  new_comment = Comment( content  = content
                       , creator  = username
                       , parent   = Post.objects.get(id=int(id))
                       , creators = creator_info
                       )
  new_comment.save()

  return HttpResponseRedirect("/")

