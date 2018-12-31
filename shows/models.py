# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from actors.models import Actors

class Shows(models.Model): 
	title = models.CharField(max_length=300, null = True)
	year = models.IntegerField(null=True)
	date = models.DateField(null=True)
	follower_count = models.IntegerField(null=False, default=0)
	favorited_count = models.IntegerField(null=False, default=0)
	url = models.CharField(max_length=200, null=True)
	image_preview = models.CharField(max_length=1000, null=True)
	page_visits = models.IntegerField(default=0)
	summary = models.CharField(max_length=500, null=True)
	num_episodes = models.IntegerField(null=True)
	english_title = models.CharField(max_length=300, null=True)
	genres = models.CharField(max_length=300, null=True)
	alternate_names = models.CharField(max_length=300, null=True)
	actor_roles = models.ManyToManyField('ActorRoles', related_name='shows_actor_roles')

	follower_count = models.IntegerField(default=0)
	favorited_count = models.IntegerField(default=0)

class ActorRoles(models.Model): 
	show = models.ForeignKey(Shows, on_delete=models.CASCADE)
	actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
	is_lead = models.BooleanField(null=False, default=False)
	role_name = models.CharField(max_length=200, null=True)
