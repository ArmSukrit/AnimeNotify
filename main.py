import concurrent.futures
import csv
import os
import sys
from threading import Thread
from time import sleep

limit = 2
for i in range(3):
    try:
        from checkers import *
        from constants import CONNECTION_ERROR_FLAG
        from exceptions import CannotCheckError
        from gui import AddApp, ReportApp
        from utils import (URLS_FILE, CompareResult, compare, see_url_structs,
                           wait_for_internet, wait_key)
    except ImportError:
        if i == limit:
            print("Cannot install dependencies...")
            exit(1)
        print("Installing dependencies...")
        os.system(sys.executable + " -m pip install -r requirements.txt")
        os.system("cls")
    else:
        break


# each key of checkers dict is something common across urls from the same website --------------------------------------
INSTALLED_CHECKERS = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
    "kissanimes.tv": kissanimes_tv_checker,
    "youtube.com/playlist?list=": youtube_playlist_checker,
    "crunchyroll": crunchyroll_checker,
    "anime-master": anime_master_checker,
    "anime-sugoi": anime_sugoi_checker,
    "fairyanime": fairyanime_checker,
    "animekimi": animekimi_checker,
    "anime-kimuchi": anime_kimuchi_checker,
    "anime-teri": anime_teri_checker,
    "akaanime": akaanime_checker,
    "hereanime": hereanime_checker,
    "anime-i": anime_i_checker,
    "mio-anime": mio_anime_checker,
    "gg-anime": gg_anime_checker,
    "shibaanime": shibaanime_checker,
    "animelizm": animelizm_checker,
    "i-moviehd": i_movie_hd_checker,
    "gogoanime": gogoanime_checker,
    "animefreak": animefreak_checker,
    "chia-anime": chia_anime_checker,
    "boss-anime": boss_anime_checker,
    "animeseesan": animeseesan_checker,
    "pokemon-th": pokemon_th_checker,
    "anime-thai": anime_thai_checker,
    "ok-anime": ok_anime_checker,
    "king-anime": king_anime_checker,
    "animelolo": animelolo_checker,
    "anime-gg": anime_gg_checker,
    "neko-miku": neko_miku_checker,
    "cat2auto": cat2auto_checker,
    "animeindy": animeindy_checker,
    "do-anime": do_anime_checker,
    "dutoon.com": dutoon_checker,
    "animemala": animemala_checker,
    "anifume": anifume_checker,
    "merlin-anime": merlin_anime_checker,
    "ki-anime": ki_anime_checker,
    "cartoonsubthai": cartoonsubthai_checker,
    "anime-suba": anime_suba_checker,
    "otaame": otaame_checker,
    "animelucky.com": animelucky_checker,
    "anime-hub": anime_hub_checker,
    "animehdzero": animehdzero_checker,
    "xn--12c1ca5a8bpx4a4bxe": doo_anime_sanook_checker,
    "anime-daisuki.net": anime_daisuki_net_checker,
    "123-hd": one23_hd_checker,
    "series-dd": series_dd_checker,
}


# ----------------------------------------------------------------------------------------------------------------------

def main():

    # read urls from csv
    data, duplicate_urls = read_info(constants.info_file)
    data.sort(key=lambda each: each["title"])
    print_what_to_check(data)
    if duplicate_urls:
        report_duplicates(duplicate_urls)

    # check each url using threading
    pause = False
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [result for result in executor.map(
            check, data) if result is not None]
        if CONNECTION_ERROR_FLAG in results:
            wait_key("Check your internet, then try again.")
            exit(1)
        if False in results:
            # False is returned by check function if Checker for {url} is not found or not installed, or key is incorrect
            # or Checker doesn't work for some reasons to be investigated
            pause = True

            # filter results that went wrong out
            results = [result for result in results if result != False]

    # results is a list of utils.CompareResult(s)
    if results:
        save(results)

        # filter results so that the gui launches only if found new ep when there is old ep in save file
        distint_new_ep_results = []
        for compare_result in results:
            if compare_result.old_ep is None:
                continue
            if compare_result not in distint_new_ep_results:
                # CompareResult objects are considered the same if their title attributes are the same
                distint_new_ep_results.append(compare_result)

        if distint_new_ep_results:
            ReportApp(distint_new_ep_results).run()
        else:
            if not pause:
                sleep(3)
            else:
                wait_key()
    else:
        print("\nNo update is found.")
        if not pause:
            sleep(3)
        else:
            wait_key()
    # end of program


def print_what_to_check(data: list):
    distint_titles = set([v["title"] for v in data])
    print(f"Checking {len(distint_titles)} titles")
    i = 1
    for k in range(len(data)):
        try:
            if data[k]['title'] == data[k - 1]['title']:
                print(
                    f"{' ' * (i//10 + 5)}{data[k]['title']}  {data[k]['url']}")
            else:
                print(f"{i:3}  {data[k]['title']}  {data[k]['url']}")
                i += 1
        except IndexError:
            pass

    print("_________________________________________________________________________________________________________\n")


def read_info(file, stop=False):
    """return list[dict], keys in dict are 'url', 'ep', 'title' and set of duplicate urls if there is any  """

    if not os.path.exists(file):
        with open(file, 'w') as new_file:
            new_file.write(','.join(constants.field_names) + '\n')
        t = Thread(target=see_url_structs)
        t.start()

    data = []
    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=constants.field_names)
        read_urls = []
        duplicates = set()
        for line in reader:
            if line['url'] == "url":
                continue
            data_dict = {
                "url": line['url'],
                'ep': int(line['ep']) if line['ep'] else None,
                'title': line['title']
            }
            if line['url'] not in read_urls:
                data.append(data_dict)
                read_urls.append(line['url'])
            else:
                duplicates.add(line['url'])

    if not data and not stop:
        os.system("cls")
        print("No saved urls in urls.csv.\nAdd some then\nPress any key to continue...")
        sleep(2)
        t = Thread(target=run_addapp, name="run add app")
        t.start()
        wait_key()
        data, duplicates = read_info(file, stop=True)

    if not data:
        print("You have not added urls to urls.csv, try again later. D:")
        sleep(5)
        exit(1)

    os.system("cls")

    return data, duplicates


def report_duplicates(duplicates):
    printed_urls = []
    for url in duplicates:
        if url not in printed_urls:
            print(f"Found multiple of {url} in {constants.info_file}.")
            printed_urls.append(url)
    print()


def check(info):
    """
    :param info: list of dict
    :return: CompareResult if found new ep else None
    """

    url = info['url']
    for key in INSTALLED_CHECKERS.keys():
        if key in url:
            checker = INSTALLED_CHECKERS[key]
            try:
                return compare(checker, info)
            except CannotCheckError:
                return False
    print(
        f"Checker for {url} is not found or not installed, or key is incorrect.\n")
    return False


def save(results: CompareResult, file=constants.info_file):
    """returns True if new url is added to checklist else False"""

    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        added = False
        ignored_titles = []  # to ignore same title with diff urls
        ignored_lines = []  # to ignore modified lines as index
        for result in results:
            if result.title in ignored_titles:
                continue
            for i, line in enumerate(lines):
                if i in ignored_lines:
                    continue
                if result.title in line:
                    ignored_titles.append(result.title)
                    line = line.rstrip()
                    if result.old_ep:
                        components = line.split(',')
                        # replace old ep with new ep
                        line = ','.join(
                            components[:2]) + ',' + str(result.current_ep)
                    else:
                        added = True
                        if line[-1] != ',':
                            line += ','
                        line += str(result.current_ep)
                        print(
                            f"Added '{result.title}' to checklist. (current ep {result.current_ep})")
                    line += '\n'
                    lines[i] = line
                    ignored_lines.append(i)
        if lines[-1][-1] != "\n":
            lines[-1][-1] += '\n'
        f.writelines(lines)
        if added:
            print()
        return added


def run_addapp():
    AddApp().run()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
