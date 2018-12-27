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
        print("Beginning actor cron job...")
        for actor in Actors.objects.all():
            print("Begin adding actor "+actor.native_name+" into database...")
            info = parseExternalURL(actor.external_url, actor)
            print("Finished parsing information...")
            if info: 
                for show in info: 
                    title = show['title']
                    year = show['year']

                    date = show['date']
                    if date:
                        date_list = date.split("-")
                        for d in range(len(date_list)):
                            if int(date_list[d]) < 1: 
                                date_list[d] = "01"

                        date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

                    url = show['url']
                    image = show['image']

                    #performs a check to make sure that the show title isn't already in the db
                    show_exists = Shows.objects.filter(title=title).exists()
                    if not show_exists: 
                        try:
                            s = Shows(title=title, year=year, url=url, image_preview=image, date=date)
                            s.save()
                            
                            role = show["role"]
                            a = ActorRoles(show=s, actor=actor, role_name=role)
                            a.save()
                            
                            s.actor_roles.add(a)
                            s.save()
                        except:
                            print("saving in updateActorInfo didn't work")
                    elif show_exists and date:
                        s = Shows.objects.get(title=title)
                        s.date = date
                    else:
                        print("No information to parse!")
            try:
                print("actor last updated")
                actor.last_updated = datetime.date.today()
                actor.save()
            except:
                print("updateActorInfo: actor didn't save")
            print("Completed adding actor "+ actor.native_name + " into database. Added all shows.")
        print("Actor cron job complete!")

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
    print("Parsing...")
    BAIDU_URL = "https://baike.baidu.com"
    info = []
    movies_dramas = soup.find_all("div", class_="starMovieAndTvplay")
    dramas_string = movies_dramas[baidu_index]
    dramas = dramas_string.select(".listItem")
    for drama in dramas: 
        title = drama.find_all("b", {"class":"title"})[0].text
        #want to adjust title if there are link brackets at the end
        if "[" in title: 
            title = title[:title.find("[")]

        url = drama.find_all("a", href=True, limit=1)[0]
        image = str(url.find_all("img", limit=1))
        #hard code getting image...
        first = image.index('"')
        image = image[first+1:-4] #hard coded, meh
        ind_drama = {}

        ind_drama["title"] = title
        ind_drama["url"] = BAIDU_URL + url['href']
        ind_drama["image"] = image

        date = drama.select("b")[1].text
        ind_drama["year"] = date.split("-")[0]
        if "-" in date:
            ind_drama["date"] = date
        else: 
            ind_drama["date"] = None

        role = drama.select("dd")[0].text
        ind_drama["role"] = role

        info.append(ind_drama)
    return info


        