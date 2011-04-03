from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from wall.posts.models import Post, Comment
from wall.users.models import UserProfile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
from django.contrib import messages
import datetime


def home(request):
  return home_paginated(request, "1")

def home_redirect(request):
  return HttpResponsePermanentRedirect("/")

def home_paginated(request, page):
  user_info = get_user_info(request.user.username, request.user)

  candidates = User.objects.filter(userprofile__is_special=True).order_by('-userprofile__challenges_answered')

  p = Paginator(Post.objects.all().order_by('-date_bumped'), 5)

  num_pages = p.num_pages
  displayed_page_range = [str(x) for x in range(max(int(page) - 2, 1), min(int(page) + 2, num_pages) + 1)]

  if request.user.is_authenticated() and request.user.facebook_profile.is_authenticated():
    for notification in request.user.get_profile().notifying_set.all():
      link = " <a href='/postdetail/%d/'>Link.</a>" % notification.parent.id
      messages.add_message(request, messages.INFO, notification.content + link)
      notification.notifying.remove(request.user.get_profile())

  
  return render_to_response( "index.html"
                           , { "posts"        : p.page(int(page)).object_list
                             , "loggedin"     : request.user.is_authenticated() and request.user.facebook_profile.is_authenticated()
                             , "user"         : request.user
                             , "user_info"    : user_info
                             , "candidates"   : candidates
                             , "page_range"   : displayed_page_range
                             , "current_page" : page
                             }
                           , context_instance=RequestContext(request)
                           )

def get_user_info(username, user):
  creator_info = None

  if user.is_authenticated() and user.facebook_profile.is_authenticated():
    creator_info = User.objects.get(username=user.username).get_profile()
  else:
    creator_info = get_anon_user_info()

  return creator_info

def get_anon_user_info():
  info = None
  #Create only if necessary
  try:
    info = User.objects.get(is_anon=True)
  except:
    info = UserProfile(is_special=False, is_anon=True)
  
  return info


def post_detail(request, id):
  post = Post.objects.get(id=int(id))

  return render_to_response( "postdetail.html"
                           , { "post" : post
                             }
                           , context_instance=RequestContext(request)
                           )


def post_post(request):
  content         = request.POST["content"]
  username        = request.POST["name"]
  creator_info    = get_user_info(username, request.user)
  is_challenge    = ("challenge" in request.POST)
  challenged_user = None
  time            = datetime.datetime.now()

  if is_challenge:
    try:
      challenged_user = User.objects.get(username=request.POST["candidate"])
    except:
      messages.error(request, "Couldn't find that user!")
      return HttpResponseRedirect("/")
    
    if challenged_user == request.user:
      messages.error(request, "Cheater! You can't challenge yourself!")
      return HttpResponseRedirect("/")
    
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
  creator_info = get_user_info(username, request.user)
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
        messages.error(request, "You already responded to that challenge!")
        return HttpResponseRedirect("/")
    else:
      messages.error(request, "That challenge isn't directed at you!")
      return HttpResponseRedirect("/")


  new_comment = Comment( content      = content
                       , creator      = username
                       , parent       = parent
                       , creators     = creator_info
                       , date_created = datetime.datetime.now()
                       )
  new_comment.save()

  #Figure out who we have to notify.

  #Everyone who commented
  for comment in parent.comment_set.all():
    new_comment.notifying.add(comment.creators)

  #Also notify the creator of the thread
  new_comment.notifying.add(parent.creators)

  new_comment.save()

  return HttpResponseRedirect("/")
