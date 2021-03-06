from django.conf.urls import url, include

from actors import views as actor_views

urlpatterns = [
    url(r'^$', actor_views.actors_home, name='actors-home'),
    url(r'^add_actor$', actor_views.add_actor, name='add-actor'),
    url(r'^create_actor/$', actor_views.create_actor, name='create-actor'), 
    url(r'^follow_actor/$', actor_views.follow_actor, name='follow-actor'),
    url(r'^favorite_actor/$', actor_views.favorite_actor, name='favorite-actor'),
    url(r'^(?P<actor_id>[0-9]*)$', actor_views.find_actor, name='find-actor'),
]