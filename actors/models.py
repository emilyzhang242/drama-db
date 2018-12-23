from django.db import models
from django.contrib.auth.models import User

class Actors(models.Model):
    stage_name = models.CharField(max_length=200, null=False)
    birth_name = models.CharField(max_length=200, null=False)
    age = models.DateTimeField(null=True)
    native_name = models.CharField(max_length=200, null=False)
    nationality = models.CharField(max_length=200, null=False)
    gender = models.IntegerField(default=0) #0 is male, 1 is female
    added_by = models.ForeignKey(User)
