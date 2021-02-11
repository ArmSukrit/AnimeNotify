from utils import install
import global_var as gv
import requests


def anime_example_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "http://anime-example.com/{id}/"  # str(url struct of that website)

    r = requests.get(url, headers=gv.headers)
    # todo: make it return those below
    return 10, "http://anime-example.com/{id}/ep10"  # int(all eps on website), str(link to latest ep)

key = ""
checker_name = ""
url_structure = ""
checker = anime_example_checker
install(key, checker_name, url_structure, checker)