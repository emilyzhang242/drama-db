from django.db import models
from django.contrib.auth.models import User

class Actors(models.Model):
    stage_name = models.CharField(max_length=200, null=True)
    DOB = models.DateTimeField(null=True)
    native_name = models.CharField(max_length=200, null=True, unique=True)
    nationality = models.CharField(max_length=200, null=True)
    gender = models.IntegerField(default=0) #0 is male, 1 is female
    external_url = models.CharField(max_length=200, null=True)
    baidu_drama_section = models.IntegerField(null=True)
    url = models.CharField(max_length=200, null=True)
    image_url = models.CharField(max_length=1000, null=True)
    image_preview = models.CharField(max_length=1000, null=True)
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    pageviews = models.IntegerField(null=False, default=0)
    last_updated = models.DateField(null=True) #auto_now_add=True <- add this later 
    follower_count = models.IntegerField(default=0)
    favorited_count = models.IntegerField(default=0)
    page_visits = models.IntegerField(default=0)


class ActorAlternateNames(models.Model):
    actor = models.ForeignKey(Actors)

