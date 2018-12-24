from django.conf.urls import url, include

from shows import views as show_views

urlpatterns = [
    url(r'^$', show_views.shows_home, name='shows-home'),
    url(r'^create_show/$', show_views.create_show, name='create-show'), 
    url(r'^(?P<title>[a-zA-Z_+]*)$', show_views.find_show, name='find-show')
]