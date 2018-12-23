from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model): 
	user = models.OneToOneField(User)
	followed_actors = models.ManyToManyField('actors.actors', related_name="followedactors")
	favorited_actors = models.ManyToManyField('actors.actors', related_name="favoritedactors")


