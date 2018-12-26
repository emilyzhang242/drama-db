#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from actors.models import Actors
from profile.models import UserProfile
from shows.models import Shows, ActorRoles
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime
import requests
import urllib2
from bs4 import BeautifulSoup, SoupStrainer #speed up beautiful soup b/c wtf

#All of the "page" parameters will create the underline for the navbar

def actors_home(request):

	#grab actor info from models
	actors = Actors.objects.all()

	parameters = {
		"page": "people",
		"actors": actors
	}

	return TemplateResponse(
		request,
		'actors/actors_home.html',
		parameters
		)

@login_required(login_url = 'login')
def add_actor(request): 
	return TemplateResponse(
		request,
		'actors/add_actor.html',
		{"page": "people"}
		)

@login_required(login_url = 'login')
@require_POST
def create_actor(request): 
	try:
		stagename = request.POST.get("stagename")
		nativename = request.POST.get("nativename")
		nationality = request.POST.get("nationality")
		external_url = request.POST.get("url")
		baidu_drama_section = request.POST.get("baidu_section")
		gender = request.POST.get("gender")
		url = "_".join(stagename.split(" ")).lower()
		user = User.objects.get(id=request.user.id)

		#either stage or native name is the same
		exists = Actors.objects.filter(url=url).exists() or Actors.objects.filter(native_name=nativename).exists()

		if not exists:
			#alter gender status
			if gender == "Male": 
				gender = 0 
			elif gender == "Female": 
				gender = 1

			#creating instance in DB
			a = Actors(stage_name=stagename, external_url=external_url, 
				baidu_drama_section=baidu_drama_section, native_name=nativename, 
				nationality=nationality, url=url, gender=gender, added_by=user)
			a.save()
			return JsonResponse({"status": 200})
		else: 
			return JsonResponse({"status": 500, "message": "actor already exists in the database."})
	except: 
		return JsonResponse({"status": 500, "message": "creating the actor failed."})

'''This method determines whether actor info should be updated'''
def find_actor(request, stagename):
	actor = Actors.objects.get(url=stagename)
	info = []

	roles = ActorRoles.objects.filter(actor_id=actor.id)
	for role in roles: 
		ind_dict = {}
		ind_dict["role_name"] = role.role_name
		ind_dict["show"] = Shows.objects.get(id=role.show_id)
		info.append(ind_dict)

	image_url = "/images/"+actor.url+".jpg"

	#is the user following them? 
	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		if actor in profile.followed_actors.all():
			following = True
		else:
			following = False
		if actor in profile.favorited_actors.all():
			favorited = True
		else:
			favorited = False
	except:
		following = False
		favorited = False

	parameters={
		"actor": actor,
		"image": image_url,
		"info": info,
		"following_actor": following,
		"favorited_actor": favorited
	}

	return TemplateResponse(
		request,
		'actors/actor_page.html',
		parameters
	)

@login_required(login_url = 'login')
def follow_actor(request):
	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		follow = request.POST.get("follow") #wow, what a gotcha. JS true and false is diff from python!
		url = request.POST.get("actor")
		actor = Actors.objects.get(url=url)
		follower_num = actor.follower_count

		if follow == "true": 
			profile.followed_actors.add(actor)
			actor.follower_count = follower_num + 1
		else: 
			profile.followed_actors.remove(actor)
			actor.follower_count = follower_num - 1
		actor.save()
		return JsonResponse({"status":200})
	except: 
		return JsonResponse({"status": 500, "message": "Unable to follow actor"})

@login_required(login_url = 'login')
def favorite_actor(request):
	try: 
		profile = UserProfile.objects.get(user_id=request.user.id)
		favorite = request.POST.get("favorite") #wow, what a gotcha. JS true and false is diff from python!
		url = request.POST.get("actor")
		actor = Actors.objects.get(url=url)
		favorited_num = actor.favorited_count

		if favorite == "true": 
			profile.favorited_actors.add(actor)
			actor.favorited_count = favorited_num + 1
		else: 
			profile.favorited_actors.remove(actor)
			actor.favorited_count = favorited_num - 1
		actor.save()
		return JsonResponse({"status":200})
	except: 
		return JsonResponse({"status": 500, "message": "Unable to favorite actor"})



		



	






