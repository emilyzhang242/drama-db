# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles
from main.models import CronJob
import datetime
import requests
from django.utils import timezone
from bs4 import BeautifulSoup, SoupStrainer #speed up beautiful soup b/c wtf
import re

class ShowsCronJobs(CronJobBase):
    RUN_EVERY_MINS = 20 # every 2 hours
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'shows.cron_shows'    # a unique code

    def do(self):
        print("Beginning show cron job...")
        total = len(Shows.objects.all())
        for index, show in enumerate(Shows.objects.all()):
            print("Begin adding show "+ show.title +" into database. No."+str(index+1)+"/"+str(total)+"...")
            result = parseExternalURL(show.url)
            if result:
                try:
                    info = result[0]
                    show.num_episodes = info["num_episodes"]
                    show.genres = info["genres"]
                    show.alternate_names = info["alternate_names"]
                    show.english_title = info["english_title"]
                    show.save()

                    #want to add main lead info into actor roles 
                    for name in info["main_characters"]:
                        name = name.replace("\n", "").strip()
                        if result[1] == "baidu":
                            actor = Actors.objects.filter(native_name=name)
                            if actor.exists():
                                actor = actor[0]
                                role = ActorRoles.objects.filter(actor_id=actor.id, show_id=show.id)[0]
                                role.is_lead = True
                                role.save()
                except:
                    print("Couldn't parse.")
            print("Finished parsing information...")
        print("Show cron job complete!")

def parseExternalURL(url):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        page = s.get(url)
    except:
        return []
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
    if findURLtype(url) == "baidu": 
        return [parseBaiduURL(soup), "baidu"]
    elif findURLtype(url) == "mdl":
        return parseMDLURL(soup)
    else:
        return []

def findURLtype(url): 
    if "baike.baidu.com/item" in url: 
        return "baidu"
    elif "mydramalist.com/people" in url:
        return "mdl"
    else:
        return ""

def parseBaiduURL(soup):
    BAIDU_URL = "https://baike.baidu.com"
    dic = {"english_title": None, "alternate_names": None, "main_characters":[], "num_episodes": None, "genres": None}

    info = soup.find_all("div", class_="basic-info")[0]
    #hack for html to see which one is the right one to take
    search_for = [">外文名", ">其它译名", ">主", ">集", ">类"]

    info_titles = info.find_all("dt")
    info_info = info.find_all("dd")

    for index, title in enumerate(info_titles):
        title_text = str(title)
        for character in search_for:
            if character in title_text:
                if character == ">外文名":
                    dic["english_title"] = info_info[index].text.replace("\n", "")
                elif character == ">其它译名":
                    dic["alternate_names"] = info_info[index].text.replace("\n", "")
                elif character == ">主":
                    #could possibly be links, but we only want the names
                    has_a = info_info[index].find_all("a")
                    if has_a:
                        main_characters = []
                        for char in has_a:
                            main_characters.append(char.text)
                        dic["main_characters"] = main_characters
                    else:
                        if "," in info_info[index].text:
                            dic["main_characters"] = info_info[index].text.split(", ")
                        elif u'，' in info_info[index].text:
                            dic["main_characters"] = info_info[index].text.split(u'，')
                elif character == ">集":
                    eps_text = info_info[index].text
                    eps = ""
                    for i in eps_text:
                        try:
                            int(i)
                            eps += i
                        except:
                            break
                    if eps:
                        dic["num_episodes"] = int(eps)
                elif character == ">类": 
                    dic["genres"] = info_info[index].text.replace("\n", "")
    return dic

        