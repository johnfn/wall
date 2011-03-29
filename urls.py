from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'wall.posts.views.home', name='home'),
    url(r'^newpost/$', 'wall.posts.views.post_post', name='home'),
    url(r'^comment/([0-9]+)$', 'wall.posts.views.post_comment', name='home'),

    # url(r'^wall/', include('wall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
