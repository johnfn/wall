from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #===POSTS===
    url(r'^$', 'posts.views.home'),
    url(r'^1/$', 'posts.views.home_redirect'),
    url(r'^([0-9]+)/$', 'posts.views.home_paginated'),
    url(r'^newpost/$', 'posts.views.post_post'),
    url(r'^comment/([0-9]+)/$', 'posts.views.post_comment'),

    #===USERS===
    url(r'^newaccount/$', 'users.views.new_user'),
    url(r'^newaccountpost/$', 'users.views.new_user_post'),
    url(r'^support/([a-zA-Z0-9-_]+)/$', 'users.views.support_candidate'),

    url(r'^login/$', 'users.views.login_user'),
    url(r'^logout/$', 'users.views.logout_user'),

    #==FB CONNECT
    url(r'^xd_receiver\.htm.*', 'wall.users.views.xd_receiver'),


    #===CANDIDATES===
    url(r'^candidates/([a-zA-Z0-9-_]+)/$', 'wall.users.views.candidate_detail'),
    url(r'^candidates/([a-zA-Z0-9-_]+)/post/$', 'wall.users.views.candidate_post'),
    url(r'^candidates/([a-zA-Z0-9-_]+)/normal/$', 'wall.users.views.candidate_detail_force_normal'),

    # url(r'^wall/', include('wall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^facebook/', include('facebookconnect.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
