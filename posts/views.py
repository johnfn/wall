from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from wall.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
import datetime


def home(request):
  return render_to_response( "index.html"
                           , {}
                           , None 
                           )