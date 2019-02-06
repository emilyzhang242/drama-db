from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from profile.models import UserProfile, MyLists, ShowViews
from actors.models import Actors
from shows.models import Shows, ActorRoles
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
import requests
from bs4 import BeautifulSoup

#All of the "page" parameters will create the underline for the navbar

def shows_home(request):

	#grab actor info from models
	sort = request.GET.get('sort')
	shows = sort_shows(sort)
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

	paginator = Paginator(info, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	if page:
		paged_info = paginator.page(page)
	else:
		paged_info = paginator.page(1)

	parameters = {
		"page": "shows",
		"shows": shows,
		"info": paged_info,
		"sort": sort
	}

	return TemplateResponse(
		request,
		'shows/shows_home.html',
		parameters
		)

def sort_shows(sort):
	if sort == "alphabetical":
		shows = Shows.objects.order_by('title')
	else:
		shows = Shows.objects.order_by('-year')
	return shows

def find_show(request, show_id):
	show = Shows.objects.get(id=show_id)
	profile = UserProfile.objects.get(user_id=request.user.id)

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

	view = ShowViews.objects.filter(show=show, user=profile)
	status = None
	if view.exists():
		show_view = view[0]
		status = show_view.get_status_display()
	else:
		show_view = None

	list_info = []
	for l in profile.lists.all():
		temp_l = {"list": l, "show_in_list": False}
		if show in l.shows.all():
			temp_l["show_in_list"] = True
		list_info.append(temp_l)
	
	ratings = get_ratings_info(show)

	parameters={
		"show": show,
		"following_show": following,
		"favorited_show": favorited,
		"status": status,
		"show_view": show_view,
		"lists": list_info,
		"num_ratings": ratings[0],
		"rating_value": ratings[1],
		"genres": show.genres.all()
	}

	return TemplateResponse(
		request,
		'shows/show_page.html',
		parameters
	)

'''return the number of ratings and the average value'''
def get_ratings_info(show):

	views = ShowViews.objects.filter(show=show).exclude(rating=None)
	summation = 0.0
	for view in views:
		summation += view.rating
	if views:
		return len(views), summation/len(views)
	else: 
		return 0, 0

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
		favorite = request.POST.get("favorite") #wow, what a gotcha. JS true and false is diff from python!
		show_id = request.POST.get("show")
		show = Shows.objects.get(id=show_id)
		favorited_num = show.favorited_count
		if favorite == "true": 
			profile.favorited_shows.add(show)
			show.favorited_count = favorited_num + 1
		else: 
			profile.favorited_shows.remove(show)
			show.favorited_count = favorited_num - 1
		show.save()
		return JsonResponse({"status":200})
	except: 
		return JsonResponse({"status": 500, "message": "Unable to favorite show."})

@login_required(login_url = 'login')
def add_to_list(request, show_id, list_id):
	show = Shows.objects.get(id=show_id)
	mylist = MyLists.objects.get(id=list_id)

	try:
		if show not in mylist.shows.all():
			mylist.shows.add(show)
			mylist.last_updated = datetime.datetime.today()
			mylist.save()
		return JsonResponse({"status":200, "message": show.title+" has been added to list "+mylist.name})
	except:
		return JsonResponse({"status":500})

@login_required(login_url = 'login')
def update_status(request):
	status = request.POST.get("status")
	show_id = request.POST.get("show_id")

	try: 
		show = Shows.objects.get(id=show_id)
		profile = UserProfile.objects.get(user_id=request.user.id)
		view = ShowViews.objects.filter(show=show, user=profile)
		if view.exists():
			view = view[0]
			view.status = status
			view.save()
		else:
			s = ShowViews(show=show, user=profile, status=status)
			s.save()
		return JsonResponse({"status":200})
	except:
		return JsonResponse({"status":500})

@login_required(login_url = 'login')
def rate(request):
	rating = int(request.POST.get("rating"))
	show_id = request.POST.get("show_id")

	try: 
		show = Shows.objects.get(id=show_id)
		profile = UserProfile.objects.get(user_id=request.user.id)
		view = ShowViews.objects.filter(show=show, user=profile)

		if view.exists():
			view = view[0]
			view.rating = rating
			view.save()
		else:
			s = ShowViews(show=show, user=profile, rating=rating)
			s.save()
		return JsonResponse({"status":200})
	except:
		return JsonResponse({"status":500})
	
	






