# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from profile.models import UserProfile, Events, News
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
    code = 'profile.cron_profiles'    # a unique code

    def do(self):
        print("Beginning Profile Cron Job...")
        add_new_events()
        update_old_events()
        print("Finished Profile Cron Job... \n")

def add_new_events():
    for index, event in enumerate(Events.objects.all()):
        print("Starting on event " + str(index+1) + "/" + str(len(Events.objects.all())) + "...")
        for profile in UserProfile.objects.all():
            #make sure event is after last viewed to add
            if not profile.last_viewed_newsfeed or (event.time_created > profile.last_viewed_newsfeed):
                #make sure they're following the event 
                should_show = has_event_connection(event, profile)
                if should_show:
                    if not News.objects.filter(event=event, user=profile).exists():
                        n = News(event=event, user=profile) 
                        n.save()

def update_old_events():
    for profile in UserProfile.objects.all():
        newsfeed = News.objects.filter(user=profile)
        for news in newsfeed:
            if profile.last_viewed_newsfeed and profile.last_viewed_newsfeed > news.time_added:
                news.has_read = True
                news.save()

'''connection entails either they're following the show or the actor they're following acted in the show'''
def has_event_connection(event, profile):
    if event.subject == Events.SHOW:
        if event.show in profile.followed_shows.all():
            return True
        for actor in profile.followed_actors.all():
            if actor in event.show.actors.all():
                return True
    return False