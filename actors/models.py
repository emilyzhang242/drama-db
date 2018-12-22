from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=200, null=False)
    age = models.DateTimeField(null=True)
