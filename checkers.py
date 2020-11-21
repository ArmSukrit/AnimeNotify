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

each checker function needs user-defined ep function and pre-defined process function
    ep function
        return int(number of all eps), str(link to latest ep)
    process function takes the ep function and info dict
        it checks for new ep, save to csv, and report to terminal
"""

# define checkers here -------------------------------------------------------------------------------------------------

def anime_hayai_checker(info):
    def ep(url):
        r = requests.get(url, headers=gv.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        eps = [each for each in soup.find_all('p', {'style': "text-align:center"}) if ("ตอนที่ " and "HD" in each.text)
               and "แนะนำ" not in each.text]
        link = eps[-1].a['href']
        return len(eps), link

    process(ep, info)


def four_anime_to_checker(info):
    def ep(url):
        r = requests.get(url, headers=gv.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        eps = soup.find('ul', {'class': "episodes range active"}).find_all('li')
        link = eps[-1].a['href']
        return len(eps), link

    process(ep, info)


# ______________________________________________________________________________________________________________________


def save(title, ep, file=gv.info_file, old_ep=None):
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if title in line:
                line = line.rstrip()
                if old_ep:
                    components = line.split(',')
                    line = ','.join(components[:2]) + ',' + str(ep)
                else:
                    line += str(ep)
                line += '\n'
            f.write(line)


def report(title, ep, link):
    print(
        f"{title}, {ep}, {link}"
    )


def process(ep_function, info):
    current_ep, current_link = ep_function(info['url'])
    saved_ep = info['ep']
    title = info['title']
    if saved_ep is None:
        save(title, current_ep)
    else:
        if saved_ep != current_ep:
            save(title, current_ep, old_ep=saved_ep)
            report(title, current_ep, current_link)
