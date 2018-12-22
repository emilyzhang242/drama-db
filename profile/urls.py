from django.conf.urls import url, include

from profile.views import (
	newsfeed)

urlpatterns = [
    url(r'^newsfeed$', newsfeed, name='profile-newsfeed'),
]