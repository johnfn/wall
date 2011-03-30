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
    return HttpResponse("That username is already taken!")

  new_user = User.objects.create_user(username, email, password)
  new_user.save()

  new_user_extra = UserExtra(user=new_user, is_special=special, is_anon=False)
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
      return HttpResponse("That's weird. Come ask me what happened.")
  else:
    return HttpResponse("Username or password incorrect.")
    
def logout_user(request):
  logout(request)

  return HttpResponseRedirect("/")
