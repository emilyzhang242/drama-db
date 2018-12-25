# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from actors.models import Actors

class Shows(models.Model): 
	title = models.CharField(max_length=300, null = True)
	year = models.IntegerField(null=True)
	followers = models.IntegerField(null=False, default=0)
	url = models.CharField(max_length=200, null=True)
	image_url = models.CharField(max_length=200, null=True)
	page_visits = models.IntegerField(default=0)

class ActorRoles(models.Model): 
	show = models.ForeignKey(Shows)
	actor = models.ForeignKey(Actors)
	is_lead = models.BooleanField(null=False, default=False)
	role_name = models.CharField(max_length=200, null=True)
