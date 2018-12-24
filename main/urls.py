from django.conf.urls import url, include
from main import views as main_views

urlpatterns = [
    url(r'^$', main_views.main, name='main'),
    url(r'^create_account/$', main_views.create_account, name='create-account')
]