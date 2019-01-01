from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from actors.models import Actors 
from shows.models import Shows
from profile.models import UserProfile
from django.views.decorators.http import require_POST
from django.db.models import Q

def main(request):
	return TemplateResponse(
		request,
		'main/index.html', 
		{"page": ""}
	)

'''search actors and shows'''
def search(request):

	contents = request.GET.get("search")

	actors = Actors.objects.filter(Q(stage_name__icontains=contents) | Q(native_name__icontains=contents))
	shows = Shows.objects.filter(Q(title__icontains=contents) | Q(english_title__icontains=contents)
		| Q(alternate_names__icontains=contents))

	parameters = {
	"search_contents": contents,
	"actors": actors,
	"shows": shows
	}
	print("are we returning???")
	return TemplateResponse(
		request,
		'main/search.html',
		parameters
		)

@require_POST
def create_account(request):
	try:
		email = request.POST.get("email")
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
		user.save()

		#create userprofile 
		profile = UserProfile(user_id=user.id)
		profile.save()
	except: 
		print("profile could not be created")



	#TODO: perform checks to see if they exist already!! 
	return TemplateResponse(
		request,
		'main/index.html')
