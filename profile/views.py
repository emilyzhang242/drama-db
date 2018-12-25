from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from profile.models import UserProfile
from actors.models import Actors
from django.contrib.auth.decorators import login_required

@login_required(login_url = 'login')
def newsfeed(request):

	parameters = {
		'page': "profile",
		'profile_page': "Newsfeed"
	}
	return TemplateResponse(
		request,
		'profile/newsfeed.html', 
		parameters
	)

def sign_up(request):
	return TemplateResponse(
		request,
		'profile/sign-up.html'
	)

@login_required(login_url = 'login')
def people(request, filter):

	profile = UserProfile.objects.get(user_id = request.user.id)
	info = {"both":[], "followed":[], "favorited":[]}

	for actor in Actors.objects.all():
		if profile.followed_actors.filter(id=actor.id).exists() and profile.favorited_actors.filter(id=actor.id).exists():
			info["both"].append(actor)
		elif profile.followed_actors.filter(id=actor.id).exists(): 
			info["followed"].append(actor)
		elif profile.favorited_actors.filter(id=actor.id).exists(): 
			info["favorited"].append(actor)

	parameters = {
		'page': "profile",
		'filter': filter, 
		'profile_page': "People",
		'actor_info': info
	}
	return TemplateResponse(
		request,
		'profile/people.html', 
		parameters
	)