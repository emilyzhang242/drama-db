# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles
from profile.models import Events
import datetime
import requests
from django.utils import timezone
from bs4 import BeautifulSoup, SoupStrainer #speed up beautiful soup b/c wtf

class ActorsCronJobs(CronJobBase):
    RUN_EVERY_MINS = 20 # every 2 hours
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'actors.cron_actors'    # a unique code

    def do(self):
        print("Beginning actor cron job...")
        for actor in Actors.objects.all():
            print("Begin adding actor "+actor.native_name+" into database...")
            info = parseExternalURL(actor.external_url)
            if info: 
                for show in info: 
                    title = show['title']
                    year = show['year']
                    role = show["role"]

                    date = show['date']
                    if date:
                        date = format_date(date)
            
                    url = show['url']
                    image = show['image']

                    #performs a check to make sure that the show title isn't already in the db
                    show_exists = Shows.objects.filter(title=title).exists()
                    if not show_exists: 
                        try:
                            s = Shows(title=title, year=year, url=url, image_preview=image, date=date)
                            s.save()
                            s.actors.add(actor)
                            s.save()
                            
                            a = ActorRoles(show=s, actor=actor, role_name=role)
                            a.save()
                            
                            s.actor_roles.add(a)
                            s.save()

                            #update event for upcoming show
                            today = datetime.datetime.today().date()
                            if (date and date >= today) or (not date):
                                e = Events(subject=Events.SHOW, show=s, event=Events.SU)
                                e.save()
                        except:
                            print("saving in updateActorInfo didn't work")
                    else:
                        s = Shows.objects.get(title=title)
                        #update date 
                        show_date = s.date
                        #this means there was an update on when it's coming out!
                        if date and (not show_date):

                            #event update for when a show is coming out!
                            e = Events(subject=Events.SHOW, show=s, event=Events.SS)
                            e.save()

                            s.date = date
                            s.save()
                        #this code is untested!!! it's in case links are added later for actors
                        s.url = url
                        s.save()

                        #update new actor actor role for show that's already in DB
                        if not s.actor_roles.filter(actor_id=actor.id).exists():
                            a = ActorRoles(show=s, actor=actor, role_name=role)
                            a.save()

                            s.actor_roles.add(a)
                            s.save()
            try:
                actor.last_updated = datetime.date.today()
                actor.save()
            except:
                print("updateActorInfo: actor didn't save")
            print("Completed adding actor "+ actor.native_name + " into database. Added all shows.")
        print("Actor cron job complete! \n")

def format_date(date):
    date_list = date.split("-")
    for d in range(len(date_list)):
        if int(date_list[d]) < 1: 
            date_list[d] = "01"

    date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    return date

def parseExternalURL(url):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    page = s.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
    if findURLtype(url) == "baidu": 
        return parseBaiduURL(soup)
    elif findURLtype(url) == "mdl":
        return parseMDLURL(soup)
    else:
        return ""

def findURLtype(url): 
    if "baike.baidu.com/item" in url: 
        return "baidu"
    elif "mydramalist.com/people" in url:
        return "mdl"
    else:
        return ""

def parseBaiduURL(soup):
    BAIDU_URL = "https://baike.baidu.com"
    info = []

    groups = soup.find_all("div", class_="level-3")
    movies_dramas = soup.find_all("div", class_="starMovieAndTvplay")

    #find correct section for dramas 
    search_for = "参演电视剧"

    for index, html in enumerate(groups):
        text = str(html)
        if search_for in text:
            drama_index = index

    dramas_string = movies_dramas[drama_index]
    dramas = dramas_string.select(".listItem")
    for drama in dramas: 
        title_info = drama.find_all("b", {"class":"title"})[0]
        title = title_info.text
        #want to adjust title if there are link brackets at the end
        if "[" in title: 
            title = title[:title.find("[")]

        anchors = title_info.find_all("a", class_="sup-anchor")
        if anchors:
            for anchor in anchors: 
                anchor.extract()
        url = title_info.find_all("a", limit=1)
        picture = drama.find_all("div", class_="coverPic")
        if picture:
            image = str(picture[0].find_all("img", limit=1))
            #hard code getting image...
            first = image.index('"')
            image = image[first+1:-4] #hard coded, meh
        else: 
            image = None

        ind_drama = {}

        ind_drama["title"] = title
        if url:
            ind_drama["url"] = BAIDU_URL + url[0]['href']
        else:
            ind_drama["url"] = None

        ind_drama["image"] = image

        date = drama.select("b")[1].text
        ind_drama["year"] = date.split("-")[0]
        if "-" in date:
            ind_drama["date"] = date
        else: 
            ind_drama["date"] = None

        role = drama.select("dd")[0]
        poss_role = None
        if "a" in role:
            poss_role = role.filter("a")
        #chance they act as more than one character...
        if not poss_role:
            role = role.text
        else: 
            role = ""
            for r in poss_role: 
                role += r.text+"/"
            role = role[:len(role)-1]

        ind_drama["role"] = role

        info.append(ind_drama)
    return info


        