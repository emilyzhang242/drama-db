from django.db import models
from shows.models import Shows
from django.contrib.auth.models import User

class UserProfile(models.Model): 
	user = models.OneToOneField(User)
	followed_actors = models.ManyToManyField('actors.actors', related_name="followedactors")
	favorited_actors = models.ManyToManyField('actors.actors', related_name="favoritedactors")
	followed_shows = models.ManyToManyField('shows.shows', related_name="followedshows")
	favorited_shows = models.ManyToManyField('shows.shows', related_name="favoritedshows")

class ShowViews(models.Model):

	STATUS_CHOICES = (
		('C', "Completed"),
		('W', "Watching"),
		('Q', "Queued")
		)

	show = models.ForeignKey(Shows)
	user = models.ForeignKey(UserProfile)
	start_date = models.DateField(null=True, auto_now_add=True)
	end_date = models.DateField(null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)


