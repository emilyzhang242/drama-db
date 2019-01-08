# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles
from profile.models import Events
import datetime
import requests
from django.utils import timezone
import re
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

            add_actor_info(actor, info[1])

            if info[0]: 
                for show in info[0]: 
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
                            if "num_episodes" in show:
                                num_episodes = show["num_episodes"]
                                s = Shows(title=title, year=year, url=url, image_preview=image, date=date,
                                    num_episodes=num_episodes)
                            else:
                                s = Shows(title=title, year=year, url=url, image_preview=image, date=date)
                            s.save()
                            s.actors.add(actor)

                            #mdl want to save as english title, we'll go back and replace native title later
                            if "native_title" in show:
                                s.native_title = show["native_title"]
                            if "english_title" in show:
                                s.english_title = show["english_title"]
                            s.save()
                            
                            if show["role"] != None:
                                if "is_main" in show:
                                    is_lead = show["is_main"]
                                    a = ActorRoles(show=s, actor=actor, role_name=role, is_lead=is_lead)
                                    a.save()
                                else:
                                    a = ActorRoles(show=s, actor=actor, role_name=role)
                                    a.save()
                            
                                s.actor_roles.add(a)
                                s.save()
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

def add_actor_info(actor, info):
    actor.summary = info["summary"]
    actor.save()

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
    if findURLtype(url) == "baidu": 
        soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
        return parseBaiduURL(soup)
    elif findURLtype(url) == "mdl":
        soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"app"}))
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

def parseMDLURL(soup):
    MDL_URL = "https://mydramalist.com"
    info = []

    actor_info = mdl_actor_info(soup)

    drama_list = soup.find_all("table", class_="film-list")[0]
    dramas = drama_list.find_all("tr")
    if dramas:
        #ignore the header of the table
        dramas = dramas[1:]
    for drama in dramas: 
        ind_drama = {}
        ind_drama["year"] = int(drama.find_all("td", class_="year")[0].text)
        title_info = drama.find_all("td", class_="title")[0].find_all("a")[0]
        ind_drama["title"] = title_info.text
        ind_drama["english_title"] = title_info.text
        ind_drama["url"] = MDL_URL + title_info["href"]
        ind_drama["role"] = drama.find_all("td", class_="role")[0].find_all("div", class_="name")[0].text
        ind_drama["is_main"] = "Main Role" in drama.find_all("td", class_="role")[0].find_all("div", class_="roleid")[0].text
        ind_drama["num_episodes"] = int(drama.find_all("td", class_="episodes")[0].text)
        ind_drama["date"] = None
        ind_drama["image"] = None
        info.append(ind_drama)
    return info, actor_info

def mdl_actor_info(soup):
    actor_info = {"summary": ""}
    return actor_info

def parseBaiduURL(soup):
    BAIDU_URL = "https://baike.baidu.com"
    info = []
    actor_info = baidu_actor_info(soup)

    #actor_info = baidu_actor_info(soup)

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
        ind_drama["native_title"] = title
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

        ind_drama["role"] = baidu_get_role(drama)

        info.append(ind_drama)
    return info, actor_info

def baidu_get_role(info):

    dds = info.find_all("dd")
    dts = info.find_all("dt")

    for index, char in enumerate(dts): 
        if "饰演" in str(char):
            index = index

    if not index: 
        return None

    role = info.select("dd")[index]
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

    return role

def baidu_actor_info(soup):
    actor_info = {"summary": ""}

    try:
        actor_info["summary"] = get_baidu_summary(soup.find_all("div", class_="lemma-summary")[0])
    except:
        pass
    #soup = soup.find_all("div", class_='basic-info')[0]

    return actor_info

def get_baidu_summary(soup):
    text = "".join([p.text for p in soup.find_all("div", class_="para")])
    text = text.replace("\n", " ")
    text = re.sub("[\[].*?[\]]", '', text)
    return text
        