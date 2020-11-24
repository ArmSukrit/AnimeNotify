import requests
from bs4 import BeautifulSoup

import global_var as gv

"""
info is read from a line in {gv.info_file}
info = {
    'url': str,
    'ep': int or None,
    'title': str 
}

each checker function needs user-defined ep function for each website and returns called pre-defined compare function
    :param info: dict
    /* structure of checker function
    def ep():
        // todo
        return int(all eps on website), str(link to latest ep)
    return compare(ep, info) 
    */
"""

# define checkers here -------------------------------------------------------------------------------------------------

def anime_hayai_checker(info):
    """http://anime-hayai.com/"""
    def ep():
        r = requests.get(info['url'], headers=gv.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        eps = [each for each in soup.find_all('p', {'style': "text-align:center"}) if ("ตอนที่ " and "HD" in each.text)
               and "แนะนำ" not in each.text]
        link = eps[-1].a['href']
        return len(eps), link

    return compare(ep, info)


def four_anime_to_checker(info):
    """https://4anime.to/"""
    def ep():
        r = requests.get(info['url'], headers=gv.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        eps = soup.find('ul', {'class': "episodes range active"}).find_all('li')
        link = eps[0].a['href']
        return len(eps), link

    return compare(ep, info)


def kissanimes_tv_checker(info):
    """https://kissanimes.tv/"""
    def ep():
        r = requests.get(info['url'], headers=gv.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        eps = soup.find('div', {'class': "listing listing8515 full"}).find_all('a')
        return len(eps), "https://kissanimes.tv" + eps[0]['href']

    return compare(ep, info)

# ______________________________________________________________________________________________________________________


def compare(ep_function, info):
    """return CompareResult if found new ep or saved info['ep'] is None, else None"""
    current_ep, current_link = ep_function()
    saved_ep = info['ep']
    title = info['title']
    if saved_ep is None:
        return CompareResult(title, current_ep)
    else:
        if saved_ep != current_ep:
            return CompareResult(title, current_ep, current_link, saved_ep)
        else:
            return None


class CompareResult:
    def __init__(self, title, current_ep, current_link=None, old_ep=None):
        self.title = title
        self.current_ep = current_ep
        self.current_link = current_link
        self.old_ep = old_ep

    def is_found(self):
        if self.old_ep:
            return self.old_ep != self.current_ep
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}', current_ep={self.current_ep}, " \
               f"current_link='{self.current_link}', old_ep={self.old_ep})"
