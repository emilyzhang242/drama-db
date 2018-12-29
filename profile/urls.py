from django.conf.urls import url, include

from profile import views as profile_views

urlpatterns = [
    url(r'^newsfeed$', profile_views.newsfeed, name='profile-newsfeed'),
    url(r'^people/(?P<filter>[a-zA-Z]*)$', profile_views.people, name='profile-people'),
    url(r'^shows/(?P<filter>[a-zA-Z]*)$', profile_views.shows, name='profile-shows'),
    url(r'^lists/add/$', profile_views.add_list, name='profile-add-list'),
    url(r'^lists(?P<filter>[a-zA-Z]*)$', profile_views.lists, name='profile-lists'),
    url(r'^lists(?P<filter>[a-zA-Z]*)(?P<sort>[a-zA-Z]*)$', profile_views.lists, name='profile-lists'),
    url(r'^sign-up$', profile_views.sign_up, name='sign-up')
]