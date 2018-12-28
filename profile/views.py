from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from profile.models import UserProfile
from actors.models import Actors
from shows.models import Shows
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
def people(request, sort=''):

	profile = UserProfile.objects.get(user_id = request.user.id)
	info = []

	for actor in Actors.objects.all():
		if actor in profile.followed_actors.all() or actor in profile.favorited_actors.all():
			actor_dict = {"actor": actor}
			if profile.followed_actors.filter(id=actor.id).exists() and profile.favorited_actors.filter(id=actor.id).exists():
				actor_dict["followed"] = True
				actor_dict["favorited"] = True
			elif profile.followed_actors.filter(id=actor.id).exists(): 
				actor_dict["followed"] = True
				actor_dict["favorited"] = False
			elif profile.favorited_actors.filter(id=actor.id).exists(): 
				actor_dict["followed"] = False
				actor_dict["favorited"] = True
			info.append(actor_dict)

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

@login_required(login_url = 'login')
def shows(request, sort=''):

	profile = UserProfile.objects.get(user_id = request.user.id)
	info = []

	for show in Shows.objects.all():
		if show in profile.followed_shows.all() or show in profile.favorited_shows.all():
			show_dict = {"show": show}
			if profile.followed_shows.filter(id=show.id).exists() and profile.favorited_shows.filter(id=show.id).exists():
				show_dict["followed"] = True
				show_dict["favorited"] = True
			elif profile.followed_shows.filter(id=show.id).exists(): 
				show_dict["followed"] = True
				show_dict["favorited"] = False
			elif profile.favorited_shows.filter(id=show.id).exists(): 
				show_dict["followed"] = False
				show_dict["favorited"] = True
			actorroles = show.actor_roles.all()
			followed_actors = profile.followed_actors.all()
			favorited_actors = profile.favorited_actors.all()
			actors = []
			for i in actorroles: 
				actor = Actors.objects.get(id=i.actor_id)
				if actor in followed_actors or actor in favorited_actors:
					actors.append(actor)
			show_dict["actors"] = actors[:4]
			info.append(show_dict)

	parameters = {
		'page': "profile",
		'filter': filter, 
		'profile_page': "Shows",
		'show_info': info
	}
	return TemplateResponse(
		request,
		'profile/shows.html', 
		parameters
	)

@login_required(login_url = 'login')
def add_list(request):
	return TemplateResponse(
		request,
		'profile/add-list.html',
		{'profile_page': "Add to List"})

@login_required(login_url = 'login')
def lists(request):
	return TemplateResponse(
		request,
		'profile/add-list.html',
		{'profile_page': "Add to List"})


