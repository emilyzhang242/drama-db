# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles, Genres
import datetime
import requests
from django.utils import timezone
from bs4 import BeautifulSoup, SoupStrainer #speed up beautiful soup b/c wtf
import re

class ProfileCronJobs(CronJobBase):
    RUN_EVERY_MINS = 20 # every 2 hours
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'profile.cron_shows'    # a unique code

    def do(self):
        print("Beginning Profile Cron Job...")

        