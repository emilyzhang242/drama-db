from django.conf.urls import url, include

from profile.views import (
	newsfeed,
	sign_up)

urlpatterns = [
    url(r'^newsfeed$', newsfeed, name='profile-newsfeed'),
    url(r'^sign-up$', sign_up, name='sign-up')
]