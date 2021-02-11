from utils import see_url_structs
import cloudscraper
import requests
from bs4 import BeautifulSoup

import global_var as gv

# Each checker function needs to return int(all eps on website), str(link to latest ep)
# define checkers here, then install in main.py ------------------------------------------------------------------------


def anime_hayai_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "http://anime-hayai.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in soup.find_all('p', {'style': "text-align:center"}) if ("ตอนที่ " and "HD" in each.text)
           and "แนะนำ" not in each.text]
    return len(eps), eps[-1].a['href']


def four_anime_to_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://4anime.to/{category}/{title}"

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = soup.find('ul', {'class': "episodes range active"}).find_all('li')
    return len(eps), eps[-1].a['href']


def kissanimes_tv_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://kissanimes.tv/category/{title}"

    r = requests.get(url, headers=gv.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    eps = soup.find('div', {'class': "listing listing8515 full"}).find_all('a')
    return len(eps), "https://kissanimes.tv" + eps[0]['href']


def youtube_playlist_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.youtube.com/playlist?list={list_id}"

    r = requests.get(url, headers=gv.headers)
    video_ids = [each.split('"')[0] for each in r.text.split(
        '"videoId":"')][1:-3]  # 3 duplicates of each id
    return len(video_ids) // 3, f"https://www.youtube.com/watch?v={video_ids[-1]}&list=" \
                                f"{url.split('list=')[1].split('&')[0]}"


def crunchyroll_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.crunchyroll.com/{title}"

    # use this object to bypass cloudflare's bot protection (inherited from requests.Session)
    scraper = cloudscraper.create_scraper()
    r = scraper.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    last_ep = s.find('div', {"class": "wrapper container-shadow hover-classes",
                             "data-classes": "container-shadow-dark"}).find('a')
    return int(last_ep.text.split("Episode ")[1].split()[0]), "https://www.crunchyroll.com" + last_ep['href']


def anime_master_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anime-master.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find(
        'table', class_="table table-hover table-bordered").find_all('a')
    return len(eps), eps[-1]['href']


def anime_sugoi_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.anime-sugoi.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="b123").center.div.find_all('a')
    return len(eps) // 3, eps[-3]['href']


def fairyanime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://fairyanime.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find(
        'table', class_="table table-hover table-episode").find_all('tr')
    return len(eps), eps[-1].td.a['href']


def animekimi_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://animekimi.com/{category}/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('ul', class_="episodios").find_all('a')
    return len(eps), eps[-1]['href']


def anime_kimuchi_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anime-kimuchi.com/{year}/{month}/{day}/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="post-131801").find_all('div',
                                                   {'class': 'post-body'})[1].find_all('a')
    return len(eps), eps[-1]['href']


def anime_teri_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.anime-teri.com/{id}/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('ul', class_="list-ui-anime")
    return len(eps), eps[-1].center.a['href']


def akaanime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://akaanime.com/{category}/{id}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="series_ep_st").find_all('a')
    return len(eps), url  # there is no direct link to any single ep


def hereanime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://hereanime.com/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('div', class_="col-12 ep-grid")
    return len(eps), eps[-1].a['href']


def anime_i_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anime-i.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in s.find('div', class_="links").find_all(
        'a') if "hist-content" in str(each)]
    return len(eps), url + eps[-1]['href'][1:]


def mio_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.mio-anime.com/{??}/{???}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('ul', class_="list-ui-anime")
    return len(eps), eps[-1].center.a['href']


def gg_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.gg-anime.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [each for each in s.find_all(
        'h3') if 'href="https://www.anime-gg.com/watch/' in str(each)]
    return len(eps), eps[-1].span.a['href']


def shibaanime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.shibaanime.com/anime/{id}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="anime-content").find_all('p')
    return len(eps), eps[-1].a['href']


def animelizm_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.animelizm.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="mpPostList mp-group-1605").find_all('a')
    return len(eps), eps[-1]['href']


def i_movie_hd_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.i-moviehd.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('table', id="Sequel").find_all('a')
    return len(eps), eps[-1]['href']


def gogoanime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://gogoanime.so/category/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    ep = s.find('ul', id="episode_page").find('a')['ep_end']
    return int(ep), "https://gogoanime.so/" + url.split('/')[-1] + f"-episode-{ep}"


def animefreak_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.animefreak.tv/watch/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('ul', class_="check-list").find('a')
    return int(eps.text.split()[-1]), eps['href']


def chia_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "http://www.chia-anime.me/episode/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="countrydivcontainer").find_all(
        'h3', itemprop="episodeNumber")
    return len(eps), eps[0].a['href']


def boss_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://boss-anime.com/anime/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find(
        'table', class_="table table-dark table-bordered table-hover text-center text-white").find_all('a')
    return len(eps), eps[-1]['href']


def animeseesan_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://animeseesan.com/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="content").find_all('a')
    return len(eps), eps[-1]['href']


def pokemon_th_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.pokemon-th.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="entry-content entry content").find_all('p')[3:]
    return len(eps), eps[-1].a['href']


def anime_thai_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anime-thai.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="episode").find_all('a')
    return len(eps), eps[-1]['href']


def ok_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://ok-anime.com/{id?}/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="content").find_all('a')
    return len(eps), eps[-1]['href']


def king_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.king-anime.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [e for e in s.find('tbody').find_all(
        'a') if "ยังไม่มา" not in e.text]
    return len(eps), eps[0]['href']


def animelolo_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.animelolo.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = []
    for e in s.find_all('div', class_="panel-body")[2].find_all('p'):
        if not e.find('a'):
            break
        eps.append(e)
    return len(eps), eps[-1].a['href']


def anime_gg_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.anime-gg.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="mpPostList mp-group-1543").find_all('a')
    return len(eps), eps[-1]['href']


def one23_hd_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.123-hd.com/{title}-ep-{valid_ep}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('table', id="Sequel").find_all('a')
    return len(eps), eps[-1]['href']


def neko_miku_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://neko-miku.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="anime-list").find_all('a')
    return len(eps), "https://neko-miku.com" + eps[-1]['href']


def cat2auto_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://cat2auto.com/m/{id}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('div', class_="button-list")[1].find_all('a')
    return len(eps), eps[-1]['href']


def animeindy_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.animeindy.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="mpPostList mp-group-612").find_all('a')
    return len(eps), eps[-1]['href']


def do_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://do-anime.com/{id}/{title?}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [e.a for e in s.find('div', class_="col-md-12 br_top").find(
        'div', class_="text-center").div.find_all('p')]
    return len(eps), eps[-1]['href']


def dutoon_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://dutoon.com/{category}/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('ul', class_="episodios").find_all('a')
    return len(eps), eps[-1]['href']


def animemala_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://animemala.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [p.a for p in s.find(
        'div', class_="panel-body").find_all('p') if p.a is not None]
    return len(eps), eps[-1]['href']


def anifume_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anifume.com/{id}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="post-content").find_all('a')
    return len(eps), eps[-1]['href']


def merlin_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://merlin-anime.com/{category}/{id}/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="panel-body").find_all('a')
    return len(eps), eps[-1]['href']


def ki_anime_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://ki-anime.com/{id}/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', id="content").find_all('a')
    return len(eps), eps[-1]['href']


def cartoonsubthai_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.cartoonsubthai.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [tr.find('a') for tr in s.find('table', class_="table table-bordered table-hover").find(
        "tbody").find_all('tr') if "ยังไม่มา" not in str(tr)]
    return len(eps), eps[0]['href']


def anime_suba_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.anime-suba.com/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [a for a in s.find('div', class_="img01").find_all('a')
           if "ยังไม่มา" not in a.text and "รวมเรื่อง" not in a.text and "คลิกที่นี่" not in a.text]
    return len(eps), eps[-1]['href']


def otaame_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://otaame.com/{id}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = [p.a for p in s.find_all(
        'div', class_="panel-body")[3].find_all('p') if p.a is not None]
    return len(eps), eps[-1]['href']


def animelucky_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://animelucky.com/name/{id}/{title}.html"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', style="padding: 20px;font-size: 16px;").find_all('a')
    return len(eps), "https://animelucky.com" + eps[-1]['href']


def anime_hub_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.anime-hub.com/{id}/{title}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', class_="text-center").div.find_all('a')
    return len(eps), eps[-1]['href']


def animehdzero_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.animehdzero.com/catagory/{id}"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('div', style="text-align:center;")[1].find_all('a')
    return len(eps), eps[-1]['href']


def doo_anime_sanook_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://www.xn--12c1ca5a8bpx4a4bxe.com/movies/{title}/ (ดูอนิเมะสนุก.com)"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find('div', itemprop="description",
                 class_="wp-content").find_all('a')
    return len(eps), eps[-1]['href']


def anime_daisuki_net_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "https://anime-daisuki.net/{year}/{month}/{day}/{title}/"

    r = requests.get(url, headers=gv.headers)
    s = BeautifulSoup(r.text, 'lxml')
    eps = s.find_all('div', id="post-131940")[0].find_all('p')[3:-1]
    return len(eps), eps[-1].a['href']


if __name__ == "__main__":
    from sys import argv
    from utils import update_url_structs, URLS_FILE, see_url_structs
    if "-update" in argv:
        update_url_structs()
    if "-see" in argv:
        see_url_structs()
