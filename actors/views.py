from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from actors.models import Actors
from django.contrib.auth.models import User

def actors_home(request):
	return TemplateResponse(
		request,
		'actors/actors_home.html',
		{"page": "people"}
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
		stagename = request.POST.get("stagename")
		birthname = request.POST.get("birthname")
		nativename = request.POST.get("nativename")
		nationality = request.POST.get("nationality")
		url = request.POST.get("baidu")
		gender = request.POST.get("gender")
		user = User.objects.get(id=request.user.id)

		#alter gender status
		if gender == "Male": 
			gender = 0 
		elif gender == "Female": 
			gender = 1

		#creating instance in DB
		a = Actors(stage_name=stagename, birth_name=birthname, native_name=nativename,
			nationality=nationality, url=url, gender=gender, added_by=user)
		a.save()

		print("Actor Saved: " + stagename)

		#scrapeBaidu(baidu)

		return redirect('actors-home')

