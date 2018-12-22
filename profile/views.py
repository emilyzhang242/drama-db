from django.shortcuts import render
from django.template.response import TemplateResponse

def newsfeed(request):
	return TemplateResponse(
		request,
		'profile/newsfeed.html', 
		{"page": "profile"}
	)
