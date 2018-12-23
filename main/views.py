from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from profile.models import Users

def main(request):
	return TemplateResponse(
		request,
		'main/index.html', 
		{"page": ""}
	)

def create_account(request):
	if request.method == "POST":
		email = request.POST.get("email")
		username = request.POST.get("username")
		password = request.POST.get("password")
		

		user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
		user.save()

	#TODO: perform checks to see if they exist already!! 


	return TemplateResponse(
		request,
		'main/index.html')

