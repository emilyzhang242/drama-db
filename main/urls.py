from django.conf.urls import url, include

from main.views import (
	main)

urlpatterns = [
    url(r'^$', main, name='main')
]