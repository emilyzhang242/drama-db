from django.conf.urls import url, include

from profile import views as profile_views

urlpatterns = [
    url(r'^newsfeed$', profile_views.newsfeed, name='profile-newsfeed'),
    url(r'^people/(?P<filter>[a-zA-Z]*)$', profile_views.people, name='profile-people'),
    url(r'^shows/(?P<filter>[a-zA-Z]*)$', profile_views.shows, name='profile-shows'),
    url(r'^lists/add/$', profile_views.add_list, name='profile-add-list'),
    url(r'^lists/all/$', profile_views.lists, name='profile-lists'),
    url(r'^lists/delete/(?P<list_id>[0-9]*)$', profile_views.delete_list, name='profile-delete-list'),
    url(r'^lists/delete_show/$', profile_views.delete_from_list, name='profile-delete-from-list'),
    url(r'^lists/(?P<list_id>[0-9]*)$', profile_views.find_list, name='profile-find-list'),
    url(r'^lists/(?P<filter>[a-zA-Z0-9]*)(?P<sort>[a-zA-Z]*)$', profile_views.lists, name='profile-lists'),
    url(r'^sign-up$', profile_views.sign_up, name='sign-up')
]