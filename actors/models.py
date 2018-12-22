from django.db import models

class Actors(models.Model):
    name = models.CharField(max_length=200, null=False)
    age = models.DateTimeField(null=True)
    native_name = models.CharField(max_length=200, null=False)
