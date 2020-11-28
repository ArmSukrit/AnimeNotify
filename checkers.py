import cloudscraper
import requests
from bs4 import BeautifulSoup

import global_var as gv

# Each checker function needs to return int(all eps on website), str(link to latest ep)
# define checkers here, then install in main.py ------------------------------------------------------------------------

def anime_hayai_checker(url):
    """http://anime-hayai.com/{id}/"""

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in soup.find_all('p', {'style': "text-align:center"}) if ("ตอนที่ " and "HD" in each.text)
           and "แนะนำ" not in each.text]
    return len(eps), eps[-1].a['href']


def four_anime_to_checker(url):
    """https://4anime.to/{category/{title}"""

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = soup.find('ul', {'class': "episodes range active"}).find_all('li')
    return len(eps), eps[-1].a['href']


def kissanimes_tv_checker(url):
    """https://kissanimes.tv/category/{title}"""

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = soup.find('div', {'class': "listing listing8515 full"}).find_all('a')
    return len(eps), "https://kissanimes.tv" + eps[0]['href']


def youtube_playlist_checker(url):
    """https://www.youtube.com/playlist?list={list_id}"""

    r = requests.get(url, headers=gv.headers)
    video_ids = [each.split('"')[0] for each in r.text.split('"videoId":"')][1:-3]  # 3 duplicates of each id
    return len(video_ids) // 3, f"https://www.youtube.com/watch?v={video_ids[-1]}&{url.split('list=')[1]}"


def crunchyroll_checker(url):
    """https://www.crunchyroll.com/{title}"""

    # use this object to bypass cloudflare's bot protection (inherited from requests.Session)
    scraper = cloudscraper.create_scraper()
    r = scraper.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    last_ep = s.find('div', {"class": "wrapper container-shadow hover-classes",
                             "data-classes": "container-shadow-dark"}).find('a')
    return int(last_ep.text.split("Episode ")[1].split()[0]), "https://www.crunchyroll.com" + last_ep['href']


def anime_master_checker(url):
    """https://anime-master.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('table', class_="table table-hover table-bordered").find_all('a')
    return len(eps), eps[-1]['href']


def anime_sugoi_checker(url):
    """https://www.anime-sugoi.com/{id}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="b123").center.div.find_all('a')
    return len(eps) // 3, eps[-3]['href']


def fairyanime_checker(url):
    """https://fairyanime.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('table', class_="table table-hover table-episode").find_all('tr')
    return len(eps), eps[-1].td.a['href']


def animekimi_checker(url):
    """https://animekimi.com/{category}/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('ul', class_="episodios").find_all('a')
    return len(eps), eps[-1]['href']


def anime_kimuchi_checker(url):
    """https://anime-kimuchi.com/{year}/{month}/{day}/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="post-131801").find_all('div', {'class': 'post-body'})[1].find_all('a')
    return len(eps), eps[-1]['href']


def anime_teri_checker(url):
    """https://www.anime-teri.com/{id}/{title}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('ul', class_="list-ui-anime")
    return len(eps), eps[-1].center.a['href']


def akaanime_checker(url):
    """https://akaanime.com/{category}/{id}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="series_ep_st").find_all('a')
    return len(eps), url  # there is no direct link to any single ep


def hereanime_checker(url):
    """https://hereanime.com/{title}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('div', class_="col-12 ep-grid")
    return len(eps), eps[-1].a['href']


def anime_i_checker(url):
    """https://anime-i.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in s.find('div', class_="links").find_all('a') if "hist-content" in str(each)]
    return len(eps), url + eps[-1]['href'][1:]


def mio_anime_checker(url):
    """https://www.mio-anime.com/{??}/{???}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('ul', class_="list-ui-anime")
    return len(eps), eps[-1].center.a['href']


def gg_anime_checker(url):
    """https://www.gg-anime.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in s.find_all('h3') if 'href="https://www.anime-gg.com/watch/' in str(each)]
    return len(eps), eps[-1].span.a['href']


def shibaanime_checker(url):
    """https://www.shibaanime.com/anime/{id}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="anime-content").find_all('p')
    return len(eps), eps[-1].a['href']


def animelizm_checker(url):
    """https://www.animelizm.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="mpPostList mp-group-1605").find_all('a')
    return len(eps), eps[-1]['href']


def i_movie_hd_checker(url):
    """https://www.i-moviehd.com/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('table', id="Sequel").find_all('a')
    return len(eps), eps[-1]['href']


def gogoanime_checker(url):
    """https://gogoanime.so/category/{title}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    ep = s.find('ul', id="episode_page").find('a')['ep_end']
    return int(ep), "https://gogoanime.so/" + url.split('/')[-1] + f"-episode-{ep}"


def animefreak_checker(url):
    """https://www.animefreak.tv/watch/{title}"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('ul', class_="check-list").find('a')
    return int(eps.text.split()[-1]), eps['href']


def chia_anime_checker(url):
    """http://www.chia-anime.me/episode/{title}/"""

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="countrydivcontainer").find_all('h3', itemprop="episodeNumber")
    return len(eps), eps[0].a['href']
