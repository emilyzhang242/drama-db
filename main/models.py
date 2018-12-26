import json
from django.db import models
from django.utils import timezone

class CronJob(models.Model):
    last_run = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(null=False, default=False)
    error_message = models.CharField(max_length=200, null=True)