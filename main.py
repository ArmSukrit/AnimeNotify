import concurrent.futures
import csv
from gui import AddApp
import os
import sys
from time import sleep

# each key of checkers dict is something common across urls from the same website --------------------------------------
from checkers import *
from utils import compare, wait_for_internet, wait_key, update_url_structs

from exceptions import CannotCheckError

INSTALLED_CHECKERS = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
    "kissanimes.tv": kissanimes_tv_checker,
    "youtube": youtube_playlist_checker,
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
    "123-hd": one23_hd_checker,
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
}


# ----------------------------------------------------------------------------------------------------------------------

def main():
    wait_for_internet()

    # read urls from csv
    data, duplicate_urls = read_info(gv.info_file)
    print_what_to_check(data)
    if duplicate_urls:
        report_duplicates(duplicate_urls)

    # check each url using threading
    pause = False
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [result for result in executor.map(
            check, data) if result is not None]
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
        found_new_ep_results = [
            result for result in results if result.old_ep is not None]
        if found_new_ep_results:
            from gui import ReportApp
            ReportApp(found_new_ep_results).run()
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


def print_what_to_check(data):
    print(f"Checking {len(data)} titles")
    for each in data:
        print(f"- {each['title']}  ({each['url']})")
    print("_________________________________________________________________________________________________________\n")


def read_info(file):
    """return list[dict], keys in dict are 'url', 'ep', 'title' and set of duplicate urls if there is any  """

    def create_csv_if_not_exist(path):
        if not os.path.exists(path):
            with open(path, 'w') as new_file:
                new_file.write(','.join(gv.field_names) + '\n')
            return True
        return False

    while create_csv_if_not_exist(file):
        AddApp().run()
    print()

    data = []
    while True:
        with open(file, 'r', newline='') as f:
            reader = csv.DictReader(f, fieldnames=gv.field_names)
            next(reader)
            read_urls = []
            duplicates = set()
            for line in reader:
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

        if not data:
            AddApp().run()
        else:
            break

    return data, duplicates


def report_duplicates(duplicates):
    printed_urls = []
    for url in duplicates:
        if url not in printed_urls:
            print(f"Found multiple of {url} in {gv.info_file}.")
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


def save(results, file=gv.info_file):
    """returns True if new url is added to checklist else False"""

    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        added = False
        for line in lines:
            for result in results:
                if result.url in line:
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
                    break
            f.write(line)
        if added:
            print()
        return added


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
