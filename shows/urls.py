from django.conf.urls import url, include

from shows import views as show_views

urlpatterns = [
    url(r'^$', show_views.shows_home, name='shows-home'),
    url(r'^follow_show/$', show_views.follow_show, name='follow-show'),
    url(r'^favorite_show/$', show_views.favorite_show, name='favorite-show'),
    url(r'^(?P<show_id>[0-9]*)$', show_views.find_show, name='find-show')
]