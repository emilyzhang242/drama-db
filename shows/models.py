# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from actors.models import Actors
import re

class Shows(models.Model): 
	title = models.CharField(max_length=300, null = True, unique=True)

	year = models.IntegerField(null=True)
	date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	country = models.CharField(max_length=50, null=True)
	
	follower_count = models.IntegerField(null=False, default=0)
	favorited_count = models.IntegerField(null=False, default=0)
	url = models.CharField(max_length=200, null=True)
	image_preview = models.CharField(max_length=1000, null=True)
	page_visits = models.IntegerField(default=0)
	summary = models.CharField(max_length=2000, null=True)

	num_episodes = models.IntegerField(null=True)
	episodes_out = models.IntegerField(null=True)

	native_title = models.CharField(max_length=200, null=True)
	english_title = models.CharField(max_length=300, null=True)
	alternate_names = models.CharField(max_length=300, null=True)

	actor_roles = models.ManyToManyField('ActorRoles')
	actors = models.ManyToManyField('actors.Actors', related_name='shows_actors')

	num_ratings = models.IntegerField(default=0)
	
	added = models.DateTimeField(auto_now_add=True) #added into db
	last_updated = models.DateField(auto_now_add=True) #auto_now_add=True <- add this later 
	
	genres = models.ManyToManyField('Genres', related_name='shows_genre')
	follower_count = models.IntegerField(default=0)
	favorited_count = models.IntegerField(default=0)

class Genres(models.Model):
	genre = models.CharField(max_length=300, unique=True)

class ActorRoles(models.Model): 
	show = models.ForeignKey(Shows, on_delete=models.CASCADE)
	actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
	is_lead = models.BooleanField(null=False, default=False)
	role_name = models.CharField(max_length=200, null=True)
