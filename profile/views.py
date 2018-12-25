from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
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
def people(request, filter):


	parameters = {
		'page': "profile",
		'filter': filter, 
		'profile_page': "People"
	}
	return TemplateResponse(
		request,
		'profile/people.html', 
		parameters
	)