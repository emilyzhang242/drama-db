from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from profile.models import UserProfile, MyLists, ShowViews, News
from actors.models import Actors
from shows.models import Shows
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
import cgi

@login_required(login_url = 'login')
def newsfeed(request):
	profile = UserProfile.objects.get(user_id=request.user.id)

	#update when user last visited newsfeed!
	#profile.last_visited_newsfeed = datetime.now()
	#profile.save()

	news = News.objects.filter(user=profile).order_by("time_added")

	parameters = {
		'page': "profile",
		'profile_page': "newsfeed",
		'title': "Newsfeed",
		'lists': get_lists(request),
		'news': news

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
def people(request, filter, sort=''):

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
		'page': "Profile",
		'filter': filter, 
		'profile_page': "people",
		'title': "People",
		'actor_info': info,
		'lists': get_lists(request)
	}
	return TemplateResponse(
		request,
		'profile/people.html', 
		parameters
	)

@login_required(login_url = 'login')
def shows(request, filter='', sort=''):

	profile = UserProfile.objects.get(user_id = request.user.id)
	info = []

	for show in Shows.objects.all():
		showview = ShowViews.objects.filter(show=show, user=profile)
		if show in profile.followed_shows.all() or show in profile.favorited_shows.all() or showview.exists():
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
			if showview.exists():
				# adjust to match the requirements to fit the type
				show_dict["status"] = "show-"+showview[0].get_status_display().lower()
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
		'page': "Profile",
		'filter': filter, 
		'profile_page': "shows",
		'title': "Shows",
		'show_info': info,
		'lists': get_lists(request)
	}
	return TemplateResponse(
		request,
		'profile/shows.html', 
		parameters
	)

@login_required(login_url = 'login')
@require_POST
def add_list(request):
	try:
		title = cgi.escape(request.POST.get("title"))
		profile = UserProfile.objects.get(user_id=request.user.id)

		if not MyLists.objects.filter(user=profile).filter(name=title).exists():
			l = MyLists(user=profile, name=title)
			l.save()

			profile.lists.add(l)
			profile.save()

		return JsonResponse({"status": 200, "message": title})
	except:
		return JsonResponse({"status": 500})

@login_required(login_url = 'login')
def lists(request, filter='', sort=''):

	parameters = {
		'page': "Profile",
		'title': "My Lists",
		'profile_page': "mylists",
		'lists': get_lists(request)
	}

	return TemplateResponse(
		request,
		'profile/lists.html',
		parameters)

'''helper function to get lists'''
def get_lists(request):
	profile = UserProfile.objects.get(user_id=request.user.id)
	lists = profile.lists.all()
	return lists

@login_required(login_url = 'login')
def find_list(request, list_id):

	profile = UserProfile.objects.get(user_id=request.user.id)
	mylist = MyLists.objects.get(id=list_id)
	info = []

	for show in mylist.shows.all():
		show_dict = {"show": show}
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
		'page': 'Profile',
		'is_list_page': True,
		'profile_page': "mylists",
		'title': "List: "+mylist.name,
		'list': mylist,
		'lists': get_lists(request),
		'shows': info
	}

	return TemplateResponse(
		request,
		'profile/find-list.html',
		parameters)

@login_required(login_url = 'login')
@require_POST
def delete_from_list(request):
	try:
		show_id = int(request.POST.get("show_id"))
		list_id = int(request.POST.get("list_id"))

		show = Shows.objects.get(id=show_id)
		mylist = MyLists.objects.get(id=list_id)

		mylist.shows.remove(show)
		mylist.save()

		return JsonResponse({"status": 200, "message": show.title + " has been removed from list "+ mylist.name})
	except:
		return JsonResponse({"status": 500})

@login_required(login_url = 'login')
def delete_list(request, list_id):
	try: 
		mylist = MyLists.objects.get(id=list_id)
		mylist.delete()

		return redirect('profile-lists')
	except:
		return redirect('profile-find-list', list_id=mylist.id)



