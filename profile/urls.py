from django.conf.urls import url, include

from profile import views as profile_views

urlpatterns = [
    url(r'^newsfeed$', profile_views.newsfeed, name='profile-newsfeed'),
    url(r'^people(?P<filter>[a-zA-Z]*)$', profile_views.people, name='profile-people'),
    url(r'^sign-up$', profile_views.sign_up, name='sign-up')
]