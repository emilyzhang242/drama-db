from django.conf.urls import url, include

from actors import views as actor_views

urlpatterns = [
    url(r'^$', actor_views.actors_home, name='actors-home'),
    url(r'^add_actor$', actor_views.add_actor, name='add-actor'),
    url(r'^create_actor/$', actor_views.create_actor, name='create-actor')
]