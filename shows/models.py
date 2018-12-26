# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from actors.models import Actors

class Shows(models.Model): 
	title = models.CharField(max_length=300, null = True)
	year = models.IntegerField(null=True)
	follower_count = models.IntegerField(null=False, default=0)
	favorited_count = models.IntegerField(null=False, default=0)
	url = models.CharField(max_length=200, null=True)
	image_preview = models.CharField(max_length=200, null=True)
	page_visits = models.IntegerField(default=0)

class ActorRoles(models.Model): 
	show = models.ForeignKey(Shows, on_delete=models.CASCADE)
	actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
	is_lead = models.BooleanField(null=False, default=False)
	role_name = models.CharField(max_length=200, null=True)
