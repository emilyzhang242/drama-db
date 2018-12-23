from django.db import models
from django.contrib.auth.models import User

class Actors(models.Model):
    stage_name = models.CharField(max_length=200, null=True)
    birth_name = models.CharField(max_length=200, null=True)
    DOB = models.DateTimeField(null=True)
    native_name = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=200, null=True)
    gender = models.IntegerField(default=0) #0 is male, 1 is female
    external_url = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    added_by = models.ForeignKey(User, null=True)
    pageviews = models.IntegerField(null=False, default=0)
    last_updated = models.DateTimeField(null=True)
    follower_count = models.IntegerField(default=0)


class ActorAlternateNames(models.Model):
    actor = models.ForeignKey(Actors)

