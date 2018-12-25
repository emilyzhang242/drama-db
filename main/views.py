from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from profile.models import UserProfile
from django.views.decorators.http import require_POST

def main(request):
	return TemplateResponse(
		request,
		'main/index.html', 
		{"page": ""}
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
