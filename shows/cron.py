# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles, Genres
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
                    list_genres = sanitize_genres(info["genres"])
                    genres_added = add_genres(list_genres)
                    for genre in genres_added:
                        show.genres.add(genre)
                    show.alternate_names = info["alternate_names"]
                    show.english_title = info["english_title"]
                    show.summary = info["summary"]
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
        print("Show cron job complete! \n")

def sanitize_genres(list_genres):
    #possible delimiters
    if not list_genres:
        return []

    if u'、' in list_genres:
        genres = list_genres.split(u'、')
    elif "/" in list_genres:
        genres = list_genres.split("/")
    elif u'，' in list_genres:
        genres = list_genres.split(u'，')
    elif " " in list_genres:
        genres = list_genres.split(" ")
    else:
        genres = [list_genres]

    for index in range(len(genres)):
        if "[" in genres[index]: 
            genres[index] = genres[index][:genres[index].find("[")]
        genres[index] = genres[index].strip()
    return genres

def add_genres(list_genres):
    genres_added = []
    for genre in list_genres:
        try:
            poss_genre = Genres.objects.filter(genre=genre)
            if poss_genre.exists():
                genres_added.append(poss_genre[0])
            else:
                g = Genres(genre=genre)
                g.save()
                genres_added.append(g)
        except:
            pass
    return genres_added

def parseExternalURL(url):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        page = s.get(url)
    except:
        return []
    page.encoding = 'utf-8'
    soup_main = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
    soup_summary = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("body"))
    if findURLtype(url) == "baidu": 
        return [parseBaiduURL(soup_main, soup_summary), "baidu"]
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

def parseBaiduURL(soup_main, soup_summary):
    BAIDU_URL = "https://baike.baidu.com"
    dic = {"english_title": None, "alternate_names": None, "main_characters":[], "num_episodes": None, 
    "genres": None, "summary": None}

    info = soup_main.find_all("div", class_="basic-info")
    if info: 
        info = info[0]
    else: 
        return []

    #get summary
    soup_sum = soup_summary.find_all("div", class_="lemma-summary")
    if not soup_sum:
        soup_sum = soup_summary.find_all("div", class_="lemmaWgt-lemmaSummary")
    if soup_sum:
        dic["summary"] = get_baidu_summary(soup_sum[0])

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

def get_baidu_summary(soup):
    text = "".join([p.text for p in soup.find_all("div", class_="para")])
    text = text.replace("\n", " ")
    text = re.sub("[\[].*?[\]]", '', text)
    return text

        