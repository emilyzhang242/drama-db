from django.conf.urls import url, include

from actors.views import (
	actors_home, 
	add_actor)

urlpatterns = [
    url(r'^$', actors_home, name='actors-home'),
    url(r'^add_actor$', add_actor, name='add-actor')
]