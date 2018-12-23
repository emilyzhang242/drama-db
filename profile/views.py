from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

def newsfeed(request):

	if not request.user.is_authenticated: 
		return redirect('sign-up')
	else:
		User = request.user
        profile = Users.objects.get(user = User)
        parameters = {
            'user':User,
            'profile':profile,
            'page': "profile"
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