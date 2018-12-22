from django.shortcuts import render
from django.template.response import TemplateResponse

def main(request):
	return TemplateResponse(
		request,
		'main/index.html'
		)
