from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from actors.models import Actors
from django.contrib.auth.models import User

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
		stagename = request.POST.get("stagename")
		birthname = request.POST.get("birthname")
		nativename = request.POST.get("nativename")
		nationality = request.POST.get("nationality")
		external_url = request.POST.get("baidu")
		gender = request.POST.get("gender")
		url = "_".join(stagename.split(" "))
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

		return redirect('actors-home')

def find_actor(request, stagename):
	print stagename


