# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from actors.models import Actors
from shows.models import Shows, ActorRoles, Genres
from profile.models import Events
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
            result = parseExternalURL(show.url, show)
            if result:
                info = result[0]
                show.num_episodes = info["num_episodes"]
                if info["num_episodes_out"] != show.episodes_out and info["num_episodes_out"] != None:
                    update_episodes_out(show, info["num_episodes_out"])
                    show.episodes_out = info["num_episodes_out"]

                list_genres = sanitize_genres(info["genres"])
                genres_added = add_genres(list_genres)
                for genre in genres_added:
                    show.genres.add(genre)

                show.alternate_names = info["alternate_names"]
                show.english_title = info["english_title"]
                show.summary = info["summary"]

                today = datetime.datetime.today().date()
                if not show.date and info["date"] != None:
                    show.date = info["date"]
                    show.year = info["date"].year

                    #update event for upcoming show
                    if (info["date"] >= today):
                        if not Events.objects.filter(show=show, event=Events.SU).exists():
                            e = Events(subject=Events.SHOW, show=show, event=Events.SU)
                            e.save()

                #update event for upcoming show
                if not show.date and info["date"] == None and show.year >= today.year:
                    for actor in show.actors.all():
                        if not Events.objects.filter(show=show, event=Events.NS, actor=actor).exists():
                            e = Events(subject=Events.SHOW, show=show, event=Events.NS, actor=actor)
                            e.save()
                if not show.end_date and info["end_date"] != None:
                    show.end_date = info["end_date"]

                if not show.image_preview and info["image_preview"] != None:
                    show.image_preview = info["image_preview"]

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

        show.last_updated = datetime.datetime.today().date()
        show.save()

        print("Show cron job complete! \n")

'''we want to show only if there's a diff number of episodes out. Also, we only want to show if 
the show hasn't been added for the first time, so the check for today checks for that'''
def update_episodes_out(show, new_eps):
    if show.last_updated != datetime.datetime.today().date():
        if show.episodes_out:
            diff = new_eps-show.episodes_out
            if diff > 0: 
                e = Events(subject=Events.SHOW, show=show, event=Events.SNE, num_new_episodes=diff)
                e.save()
        else:
            e = Events(subject=Events.SHOW, show=show, event=Events.SNE, num_new_episodes=new_eps)
            e.save()

''' takes in a string of genres and returns a list of genres'''
def sanitize_genres(list_genres):
    #possible delimiters
    if not list_genres:
        return []

    if "," in list_genres:
        genres = list_genres.split(",")
    elif u'、' in list_genres:
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

def parseExternalURL(url, show):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        page = s.get(url)
    except:
        return []
    page.encoding = 'utf-8'
    if findURLtype(url) == "baidu": 
        soup_summary = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("body"))
        return [parseBaiduURL(soup_summary, show), "baidu"]
    elif findURLtype(url) == "mdl":
        soup = BeautifulSoup(page.content, "lxml", parse_only=SoupStrainer("div", {"class": "app-body"}))
        return [parseMDLURL(soup, show), "mdl"]
    else:
        return []

def findURLtype(url): 
    if "baike.baidu.com/item" in url: 
        return "baidu"
    elif "mydramalist.com/" in url:
        return "mdl"
    else:
        return ""

def parseMDLURL(soup, show):
    MDL_URL = "https://mydramalist.com"
    dic = {"english_title": show.title, "alternate_names": "", "main_characters":[], "num_episodes": None, 
    "genres": None, "summary": "", "num_episodes_out": None, "date": None, "end_date": None,
    "image_preview": None, "country": "South Korea", "native_title": None}

    #find the right box for date!
    date_content = soup.find_all("div", class_="content-side")[0].find_all("div", class_="box")
    for index, poss_boxes in enumerate(date_content):
        if poss_boxes.find_all("h3"):
            if "Details" in poss_boxes.find_all("h3")[0].text:
                date_index = index
    if date_index != None:
        dates = get_MDL_date(date_content[date_index])
        dic['date'] = dates[0]
        dic['end_date'] = dates[1]

        #can also get country 
        for i in date_content[date_index].find_all("li"):
            if "Country" in i.find_all("b")[0].text:
                dic["country"] = i.text[i.text.index(":")+1:].strip()

    details = soup.find_all("div", class_="col-lg-8")[0]
    dic["image_preview"] = details.find_all("div", class_="cover")[0].find_all("img")[0]['src']
    synopsis = details.find_all("div", class_="show-synopsis")[0].find_all("p")
    for s in synopsis:
        dic["summary"] += s.text

    show_details_box = details.find_all("div", class_="show-detailsxss")[0].find_all("ul", class_="list")[0]
    for b in show_details_box.find_all("li", class_="list-item"):
        if "Native Title" in b.find_all("b")[0].text:
            dic["native_title"] = b.find_all("a")[0].text
        elif "Also Known As" in b.find_all("b")[0].text:
            alternate_names = []
            for i in b.find_all("a"):
                alternate_names.append(i.text)
            dic["alternate_names"] = ", ".join(alternate_names)
        elif "Genres" in b.find_all("b")[0].text:
            dic["genres"] = ",".join([i.text.strip() for i in b.find_all("a")])

    return dic

def get_MDL_date(soup):
    try:
        date_info = soup.find_all("li", {"xitemprop": "datePublished"})[0].text
        has_end = "-" in date_info
        date_info = date_info[date_info.index(":")+1:].replace(",", "").strip().split("-")
        date_info[0] = re.sub(r"\s+" , " ", date_info[0].strip())
        start_date = datetime.strptime(date_info[0], '%b %d %Y').date()
        end_date = None
        if has_end: 
            date_info[1] = re.sub(r"\s+" , " ", date_info[0].strip())
            end_date = datetime.datetime.strptime(date_info[1], '%b %d %Y').date()
        return [start_date, end_date]
    except:
        return [None, None]

def parseBaiduURL(soup_summary, show):

    soup_main = soup_summary.find_all("div", class_="main-content")[0]
    dic = {"english_title": show.english_title, "alternate_names": show.alternate_names, 
    "main_characters":[], "num_episodes": show.num_episodes, 
    "genres": None, "summary": None, "num_episodes_out": None, "date": None, "country": "China",
    "end_date": None, "image_preview": show.image_preview}

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
    search_for = [">外文名", ">其它译名", ">主", ">集", ">类", "首播时间"]

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
                elif character == "首播时间":
                    dic["date"] = parse_baidu_date(info_info[index].text, show)
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
                    eps_text = info_info[index].text.strip()
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

    dic["num_episodes_out"] = get_num_episodes_out(soup_main)

    return dic

def parse_baidu_date(text, show): 
    try:
        year = int(text[:text.find(u'年')])
        month = int(text[text.index(u'年')+1: text.index(u'月')])
        day = int(text[text.index(u'月')+1: text.index(u'日')])
        date = datetime.date(year, month, day)
        return date
    except:
        return None

def get_num_episodes_out(soup):
    soup = soup.find_all("div", class_="pagers")
    if not soup:
        return None
    soup = soup[0].find_all("a")
    if soup:
        last_out = soup[-1].text
        if "-" in last_out:
            return int(last_out[last_out.index("-")+1:])
        else:
            return int(last_out)
    return None

def get_baidu_summary(soup):
    text = "".join([p.text for p in soup.find_all("div", class_="para")])
    text = text.replace("\n", " ")
    text = re.sub("[\[].*?[\]]", '', text)
    return text

        