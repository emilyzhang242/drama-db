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

	#now = datetime.date.today()
	#if actor.last_updated is not None: 
	#	time_is_same = (now == actor.last_updated)

	#if actor.last_updated is None or not time_is_same: 
	updateActorInfo(actor)

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

def updateActorInfo(actor):

	info = parseExternalURL(actor.external_url, actor)
	if info: 
		for show in info: 
			title = show['title']
			year = show['year']
			url = show['url']

			#performs a check to make sure that the show title isn't already in the db
			try:
				Shows.objects.get(title=title)
				print(title + " already exists in DB")
			except:
				try:
					s = Shows(title=title, year=year, url=url)
					s.save()
					#then actor roles 
					role = show["role"]
					a = ActorRoles(show=s, actor=actor, role_name=role)
					a.save()
				except:
					print("saving in updateActorInfo didn't work")
	else:
		print("URL PROBLEM, CAN'T PARSE")
	#update the last time the actor was updated so it won't do it every time
	# try:
	# 	actor.last_updated = datetime.date.today()
	# 	actor.save()
	# except:
	# 	print("updateActorInfo: actor didn't save")

def parseExternalURL(url, actor):
	# html = urllib2.urlopen(url).read()
	# soup = BeautifulSoup(html, "lxml")

	s = requests.Session()
	s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
	page = s.get(url)
	page.encoding = 'utf-8'
	soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
	
	if findURLtype(url) == "baidu": 
		return parseBaiduURL(soup, actor.baidu_drama_section)
	elif findURLtype(url) == "mdl":
		return parseMDLURL(soup)
	else:
		return ""

def findURLtype(url): 
	if "baike.baidu.com/item" in url: 
		return "baidu"
	elif "mydramalist.com/people" in url:
		return "mdl"
	else:
		return ""

def parseBaiduURL(soup, baidu_index):
	BAIDU_URL = "https://baike.baidu.com"
	info = []
	movies_dramas = soup.find_all("div", class_="starMovieAndTvplay")

	#this code is supposedly to automatically determine for baidu which section, but it's not working so
	#...so we'll leave it for the future I guess.

	#tags = soup.find_all("div", class_="level-3")
	#this determines the order of what we're trying to scrape for movies or dramas
	# dramas_phrase = "参演电视剧"
	# movies_phrase = "参演电影"

	# dramas_phrase = u'&#21442;&#28436;&#30005;&#35270;&#21095'; #参演电视剧
	# movies_phrase = "\xE5\x8F\x82\xE6\xBC\x94\xE7\x94\xB5\xE5\xBD\xB1" #参演电影
	# print(dramas_phrase)

	# for index, tag in enumerate(tags): 
	# 	print(tag.encode('utf-8'))
	# 	if dramas_phrase in tag:
	# 		drama_index = index
	# 	elif movies_phrase in tag:
	# 		movie_index = index

	# if not drama_index: 
	# 	return info
	# if not movie_index: 
	# 	dramas = movies_dramas[0]
	# else:
	# 	#this runs on the assumption that they're always grouped together!!!
	# 	real_index = max(drama_index-movie_index, 0)

	dramas_string = movies_dramas[baidu_index]
	dramas = dramas_string.select(".listItem .info")

	for drama in dramas: 

		title = drama.find_all("b", {"class":"title"})[0].text
		url = drama.find_all("a", href=True, limit=1)[0]
		ind_drama = {}

		ind_drama["title"] = title
		ind_drama["url"] = BAIDU_URL + url['href']

		year = drama.select("b")[1].text[:4]
		ind_drama["year"] = year

		role = drama.select("dd")[0].text
		ind_drama["role"] = role

		info.append(ind_drama)

	return info

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



		



	






