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
def create_actor(request): 
	if request.method == "POST":
		try:
			stagename = request.POST.get("stagename")
			birthname = request.POST.get("birthname")
			nativename = request.POST.get("nativename")
			nationality = request.POST.get("nationality")
			external_url = request.POST.get("baidu")
			gender = request.POST.get("gender")
			url = "_".join(stagename.split(" ")).lower()
			user = User.objects.get(id=request.user.id)

			#alter gender status
			if gender == "Male": 
				gender = 0 
			elif gender == "Female": 
				gender = 1

			#creating instance in DB
			a = Actors(stage_name=stagename, external_url=external_url, birth_name=birthname, 
				native_name=nativename, nationality=nationality, url=url, gender=gender, added_by=user)
			a.save()
		except: 
			print("create_actor failed")
		return redirect('actors-home')

'''This method determines whether actor info should be updated'''
def find_actor(request, stagename):
	actor = Actors.objects.get(url=stagename)

	now = datetime.datetime.now()
	print(now)
	if actor.last_updated is not None: 
		time_diff = (now-actor.last_updated).total_seconds()/3600

	if actor.last_updated is None or time_diff >= 24: 
		updateActorInfo(actor)

	image_url = "/images/"+actor.url+".jpg"
	parameters={
		"actor": actor,
		"image": image_url
	}

	return TemplateResponse(
		request,
		'actors/actor_page.html',
		parameters
	)

def updateActorInfo(actor):

	info = parseExternalURL(actor.external_url)
	print(info)
	if info: 
		for show in info: 
			title = show['chinese_title']
			year = show['year']
			s = Shows(chinese_title=title, year=year)
			s.save()
			#then actor roles 
			role = show["role"]
			a = ActorRoles(show=s, actor=actor, role_name=role)
			a.save()
	else:
		print("WRONG URL, CAN'T PARSE")

	#for show in info: 
	# add into the database

def parseExternalURL(url):
	s = requests.Session()
	s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
	page = s.get(url)
	page.encoding = 'utf-8'
	soup = BeautifulSoup(page.content, "html.parser")

	if findURLtype(url) == "baidu": 
		return parseBaiduURL(soup)
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

def parseBaiduURL(soup):
	movies_dramas = soup.find_all("div", class_="starMovieAndTvplay")
	dramas_string = movies_dramas[1]
	dramas = dramas_string.select(".listItem .info")

	info = []
	for drama in dramas: 
		ind_drama = {}
		ind_drama["title"] = ""

		chinese_title = drama.find_all("b", {"class":"title"})[0].text
		ind_drama["chinese_title"] = chinese_title

		year = drama.select("b")[1].text[:4]
		ind_drama["year"] = year

		role = drama.select("dd")[0].text
		ind_drama["role"] = role

		info.append(ind_drama)
	return info



	






