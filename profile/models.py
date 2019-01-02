from django.db import models
from shows.models import Shows
from actors.models import Actors
from django.contrib.auth.models import User

class UserProfile(models.Model): 
	user = models.OneToOneField(User)
	last_viewed_newsfeed = models.DateTimeField(null=True)
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
	rating = models.FloatField(null=True)

class MyLists(models.Model):
	user = models.ForeignKey(UserProfile)
	name = models.CharField(max_length=200, null=True)
	shows = models.ManyToManyField(Shows)
	date_created = models.DateField(auto_now_add=True)
	last_updated = models.DateField(auto_now_add=True)

class Events(models.Model): 

	SHOW = "SHOW"
	ACTOR = "ACTOR"

	SS, SU, SNE, ANS = "SS", "SU", "SNE", "ANS"

	SUBJECTS = (
		(SHOW, "Shows"),
		(ACTOR, "Actors")
		)

	EVENTS = (
		(SS, "Show Started"), #show started broadcasting ie there's a date now,
		(SU, "Show Upcoming"), #show will show sometime in the future, no date or future date
		(SNE, "Show New Episode") #NOT DONE YET
		)

	subject = models.CharField(max_length=20, choices=SUBJECTS, null=True)
	show = models.ForeignKey(Shows)
	event = models.CharField(max_length=20, choices=EVENTS, null=True)
	time_created = models.DateTimeField(auto_now_add=True)

class NewsFeed(models.Model):
	event = models.ForeignKey(Events)
	user = models.ForeignKey(UserProfile)
	has_read = models.BooleanField(default=False)
	has_deleted = models.BooleanField(default=False)
	time_added = models.DateTimeField(auto_now_add=True)
	is_saved = models.BooleanField(default=False) 



