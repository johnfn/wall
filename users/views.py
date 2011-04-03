from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from wall.posts.models import Post, Comment
from wall.users.models import UserProfile, CandidateInfo
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
from django.contrib import messages
import datetime

def new_user(request):
  return render_to_response( "newuser.html"
                           , {}
                           , context_instance=RequestContext(request)
                           )


def new_user_post(request):
  username = request.POST["name"]
  email    = request.POST["email"]
  password = request.POST["password"]
  special  = 'special' in request.POST

  #TODO: Not count. exists maybe?
  if User.objects.filter(username=request.POST.get('username')).count() > 0:
    messages.add_message(request, messages.INFO, 'That username is already taken!')
    return HttpResponseRedirect("/")

  new_user = User.objects.create_user(username, email, password)
  new_user.save()

  new_user_extra = UserProfile( user       = new_user
                              , is_special = special
                              , is_anon    = False
                              , challenges = 0
                              , challenges_answered = 0
                              , supporters = 0
                              )
  new_user_extra.save()

  #If it's a candidate, give him some corresponding info as well.
  if special:
    new_user_info = CandidateInfo( content = ""
                                 , picture = ""
                                 )
    new_user_info.save()
    new_user_extra.info = new_user_info
    new_user_extra.save()
  
  #Now log him in.
  user = authenticate(username=username, password=password)
  login(request, user)

  return HttpResponseRedirect("/")


def login_user(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      return HttpResponseRedirect("/")
    else:
      messages.error(request, 'Your username is inactive. Maybe you were banned? Tweet us.')
      return HttpResponse("/")
  else:
    messages.error(request, 'Incorrect username or password.')
    return HttpResponse("/")

def logout_user(request):
  logout(request)
  return HttpResponseRedirect("/")

def get_cand_prof(candidate):
  user = User.objects.get(username=candidate)
  prof = user.get_profile()
  return prof

def candidate_detail(request, candidate):
  cand_prof = get_cand_prof(candidate)
  challenges = Post.objects.filter(challenged_user=User.objects.get(username=candidate))

  return render_to_response( "candidate.html"
                           , { "candidate"    : cand_prof
                             , 'is_candidate' : candidate == request.user.username
                             , "challenges"   : challenges
                             }
                           , context_instance=RequestContext(request)
                           )

def candidate_detail_force_normal(request, candidate):
  cand_prof = get_cand_prof(candidate)
  challenges = Post.objects.filter(challenged_user=User.objects.get(username=candidate))

  return render_to_response( "candidate.html"
                           , { "candidate"    : cand_prof
                             , "is_candidate" : False
                             , "challenges"   : challenges
                             }
                           , context_instance=RequestContext(request)
                           )


def candidate_post(request, candidate):
  cand_info = get_cand_info(candidate)
  cand_info.content = request.POST["content"]
  cand_info.save()
  messages.success(request, 'Your changes were saved successfully!')
  return HttpResponseRedirect("/candidates/%s/" % candidate)

def support_candidate(request, candidate):
  if not request.user.is_authenticated() or not request.user.facebook_profile.is_authenticated():
    messages.warning(request, "You must log in using Facebook connect to support a candidate.")
    return HttpResponseRedirect("/")

  try:
    new_user = User.objects.get(username=candidate)
  except:
    messages.error(request, "User '%s' does not exist!" % candidate)
    return HttpResponseRedirect("/")
  
  if new_user == request.user:
    messages.error(request, "Yeah, right! You can't support yourself!")
    return HttpResponseRedirect("/")
  
  old_user = request.user.get_profile().supports
  if old_user is not None:
    old_user.get_profile().supporters -= 1
    old_user.get_profile().save()
  
  new_user.get_profile().supporters += 1
  new_user.get_profile().save()

  prof = request.user.get_profile()
  prof.supports = new_user
  prof.save()
  
  messages.success("You are now supporting <strong>%s</strong>!" % new_user.get_full_name())
  return HttpResponseRedirect("/")

def xd_receiver(request):
  return render_to_response('xd_receiver.html')