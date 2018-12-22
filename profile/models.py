from django.db import models

class Users(models.Model): 
	username = models.CharField(max_length=200, null=False)
	email = models.CharField(max_length=200, null=False)
	password = models.CharField(max_length=200, null=False)
	followed_actors = models.ManyToManyField('actors.actors', related_name="followed_actors")


