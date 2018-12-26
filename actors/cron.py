from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles
from main.models import CronJob
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
        error_message = ""
        try:
            print("Beginning actor cron job...")
            for actor in Actors.objects.all():
                print("Begin adding actor "+actor.native_name+" into database.")
                info = parseExternalURL(actor.external_url, actor)
                if info: 
                    for show in info: 
                        title = show['title']
                        year = show['year']
                        url = show['url']

                        #performs a check to make sure that the show title isn't already in the db
                        try:
                            Shows.objects.get(title=title)
                        except:
                            try:
                                s = Shows(title=title, year=year, url=url)
                                s.save()
                                #then actor roles 
                                role = show["role"]
                                a = ActorRoles(show=s, actor=actor, role_name=role)
                                a.save()
                            except:
                                print("saving in updateActorInfo didn't work")
                else:
                    error_message = "URL PROBLEM, CAN'T PARSE"
                    print("URL PROBLEM, CAN'T PARSE")
                try:
                    actor.last_updated = datetime.date.today()
                    actor.save()
                except:
                    error_message = "updateActorInfo: actor didn't save"
                    print("updateActorInfo: actor didn't save")
                print("Completed adding actor "+ actor.native_name + " into database. Added a total of "+ len(info)+ " shows.")
            c = CronJob(successful=True)
            c.save()
        except: 
            c = CronJob(error_message=error_message)
            c.save()

def parseExternalURL(url, actor):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    page = s.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class":"main-content"}))
    if findURLtype(url) == "baidu": 
        return parseBaiduURL(soup, actor.baidu_drama_section)
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

def parseBaiduURL(soup, baidu_index):
    BAIDU_URL = "https://baike.baidu.com"
    info = []
    movies_dramas = soup.find_all("div", class_="starMovieAndTvplay")

    dramas_string = movies_dramas[baidu_index]
    dramas = dramas_string.select(".listItem .info")

    for drama in dramas: 

        title = drama.find_all("b", {"class":"title"})[0].text
        url = drama.find_all("a", href=True, limit=1)[0]
        ind_drama = {}

        ind_drama["title"] = title
        ind_drama["url"] = BAIDU_URL + url['href']

        year = drama.select("b")[1].text[:4]
        ind_drama["year"] = year

        role = drama.select("dd")[0].text
        ind_drama["role"] = role

        info.append(ind_drama)

    return info


        