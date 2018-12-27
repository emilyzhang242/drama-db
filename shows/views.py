from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from profile.models import UserProfile
from actors.models import Actors
from shows.models import Shows, ActorRoles
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime
import requests
from bs4 import BeautifulSoup

#All of the "page" parameters will create the underline for the navbar

def shows_home(request):

	#grab actor info from models
	shows = Shows.objects.all()
	info = []

	for show in shows: 
		d = {"show":show}
		actorroles = show.actor_roles.filter(show_id=show.id)[:3]
		actors = []
		for role in actorroles:
			actors.append(Actors.objects.get(id=role.actor_id))
		d["shows"] = shows
		d["actors"] = actors
		info.append(d)

	parameters = {
		"page": "shows",
		"shows": shows,
		"info": info
	}

	return TemplateResponse(
		request,
		'shows/shows_home.html',
		parameters
		)

'''This method determines whether actor info should be updated'''
def find_show(request, show_id):
	show = Shows.objects.get(id=show_id)

	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		if show in profile.followed_shows.all():
			following = True
		else:
			following = False
		if show in profile.favorited_shows.all():
			favorited = True
		else:
			favorited = False
	except:
		following = False
		favorited = False
	
	parameters={
		"show": show,
		"following_show": following,
		"favorited_show": favorited
	}

	return TemplateResponse(
		request,
		'shows/show_page.html',
		parameters
	)

@login_required(login_url = 'login')
def follow_show(request):
	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		follow = request.POST.get("follow") #wow, what a gotcha. JS true and false is diff from python!
		show_id = request.POST.get("show")
		show = Shows.objects.get(id=show_id)
		follower_num = show.follower_count
		if follow == "true": 
			profile.followed_shows.add(show)
			show.follower_count = follower_num + 1
		else: 
			profile.followed_shows.remove(show)
			show.follower_count = follower_num - 1
		show.save()
		return JsonResponse({"status":200})
	except: 
		return JsonResponse({"status": 500, "message": "Unable to follow show"})

@login_required(login_url = 'login')
def favorite_show(request):
	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		follow = request.POST.get("follow") #wow, what a gotcha. JS true and false is diff from python!
		show_id = request.POST.get("show")
		show = Shows.objects.get(url=url)
		favorited_num = show.favorited_count

		if follow == "true": 
			profile.followed_shows.add(show)
			show.favorited_count = favorited_num + 1
		else: 
			profile.followed_shows.remove(show)
			show.favorited_count = favorited_num - 1
		show.save()
		return JsonResponse({"status":200})
	except: 
		return JsonResponse({"status": 500, "message": "Unable to follow show"})

	






