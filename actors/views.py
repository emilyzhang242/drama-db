from django.shortcuts import render
from django.template.response import TemplateResponse

def actors_home(request):
	return TemplateResponse(
		request,
		'actors/actors_home.html',
		{"page": "people"}
		)

def add_actor(request): 
	return TemplateResponse(
		request,
		'actors/add_actor.html',
		{"page": "people"}
		)
