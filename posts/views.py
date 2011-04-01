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
  user_info = get_user_info(request.user.username, request.user.is_authenticated())

  candidates = User.objects.filter(userprofile__is_special=True)
  candidates = sorted([c for c in candidates], key=lambda s: s.get_profile().challenges_answered)[::-1]

  #TODO: .order_by('-pub_date')

  return render_to_response( "index.html"
                           , { "posts"      : Post.objects.all().order_by('-date_bumped')
                             , "loggedin"   : request.user.is_authenticated()
                             , "user"       : request.user
                             , "user_info"  : user_info
                             , "candidates" : candidates
                             }
                           , context_instance=RequestContext(request)
                           )

def get_user_info(username, authenticated):
  creator_info = None

  if authenticated:
    creator_info = User.objects.get(username=username).get_profile()
  else:
    creator_info = get_anon_user_info()

  return creator_info

def get_anon_user_info():
  info = None
  #Create only if necessary
  try:
    info = User.objects.get(is_anon=True)
  except:
    pass
    #info = UserProfile(is_special=False, is_anon=True)
  
  return info

def post_post(request):
  content         = request.POST["content"]
  username        = request.POST["name"]
  creator_info    = get_user_info(username, request.user.is_authenticated())
  is_challenge    = ("challenge" in request.POST)
  challenged_user = None
  time            = datetime.datetime.now()

  if is_challenge:
    try:
      challenged_user = User.objects.get(username=request.POST["challenged_user"])
    except:
      #TODO: Make graceful!
      return HttpResponse("Couldn't find that user!")
    
    prof = challenged_user.get_profile()
    prof.challenges += 1
    prof.save()
  
  new_post = Post( content         = content
                 , creator         = username
                 , creators        = creator_info
                 , date_created    = time

                 #Challenge stuff
                 , challenge       = is_challenge
                 , challenged_user = challenged_user
                 , date_bumped     = time
                 )
  new_post.save()

  return HttpResponseRedirect("/")

def post_comment(request, id):
  content      = request.POST["content"]
  username     = request.POST["name"]
  creator_info = get_user_info(username, request.user.is_authenticated())
  parent       = Post.objects.get(id=int(id))

  #bump parent to top
  parent.date_bumped = datetime.datetime.now()
  parent.save()

  if parent.challenge:
    if parent.challenged_user == request.user:
      if parent.challenge_answered == False:
        prof = parent.challenged_user.get_profile()
        prof.challenges_answered += 1
        prof.save()

        parent.challenge_answered = True
        parent.save()
      else:
        #TODO: Make graceful also
        return HttpResponse("You already responded to that challenge!")
    else:
      return HttpResponse("That challenge isn't directed at you!")
  

  new_comment = Comment( content  = content
                       , creator  = username
                       , parent   = parent
                       , creators = creator_info
                       )
  new_comment.save()

  return HttpResponseRedirect("/")

