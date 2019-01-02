from django.db import models
from shows.models import Shows
from django.contrib.auth.models import User

class UserProfile(models.Model): 
	user = models.OneToOneField(User)
	followed_actors = models.ManyToManyField('actors.actors', related_name="followedactors")
	favorited_actors = models.ManyToManyField('actors.actors', related_name="favoritedactors")
	followed_shows = models.ManyToManyField('shows.shows', related_name="followedshows")
	favorited_shows = models.ManyToManyField('shows.shows', related_name="favoritedshows")
	show_views = models.ManyToManyField('ShowViews', related_name="showviews")
	lists = models.ManyToManyField('MyLists')

class ShowViews(models.Model):

	COMPLETED = "C"
	WATCHING = "W"
	QUEUED = "Q"
	ABANDONED = "A"

	STATUS_CHOICES = (
		(COMPLETED, "Completed"),
		(WATCHING, "Watching"),
		(QUEUED, "Queued"),
		(ABANDONED, "Abandoned")
		)

	show = models.ForeignKey(Shows)
	user = models.ForeignKey(UserProfile)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)

class MyLists(models.Model):
	user = models.ForeignKey(UserProfile)
	name = models.CharField(max_length=200, null=True)
	shows = models.ManyToManyField(Shows)


