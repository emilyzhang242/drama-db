from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from actors.models import Actors
from shows.models import Shows, ActorRoles
from django.contrib.auth.models import User
import datetime
import requests
from bs4 import BeautifulSoup

#All of the "page" parameters will create the underline for the navbar

def shows_home(request):

	#grab actor info from models
	shows = Shows.objects.all()

	parameters = {
		"page": "shows",
		"shows": shows
	}

	return TemplateResponse(
		request,
		'shows/shows_home.html',
		parameters
		)

'''This method determines whether actor info should be updated'''
def find_show(request, show_id):
	show = Shows.objects.get(id=show_id)

	#image_url = "/images/"+actor.url+".jpg"
	parameters={
		"show": show#,
		#"image": image_url
	}

	return TemplateResponse(
		request,
		'shows/show_page.html',
		parameters
	)


	






