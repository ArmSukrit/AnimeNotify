import concurrent.futures
import csv
import os
import sys
from time import sleep

# each key of checkers dict is something common across urls from the same website --------------------------------------
from checkers import *
from utils import compare, restart, wait_for_internet, wait_key

# This bot compares the number of specific html elements against the number in save file and can optionally
# return the link to the latest ep


installed_checkers = {
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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [result for result in executor.map(
            check, data) if result is not None]

    # results is a list of utils.CompareResult(s)
    if results:
        save(results)

        # launch the gui only if found new ep when there is old ep in save file
        found_new_ep_results = [result for result in results if result.old_ep is not None]
        if found_new_ep_results:
            from gui import AnimeNotifyApp
            AnimeNotifyApp(found_new_ep_results).run()
        else:
            sleep(3)
    else:
        print("No update is found.")
        sleep(3)
    # end of program


def print_what_to_check(data):
    print("Checking...")
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

    if create_csv_if_not_exist(file):
        print(f"Add url to {gv.info_file} and save.\n"
              f"Press any key to continue...")
        sleep(1)
        os.system(file)
        wait_key()
        restart(fp=os.path.abspath(__file__), py_executable=sys.executable)

    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=gv.field_names)
        next(reader)
        data = []
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
        wait_key(f"There is no url in {gv.info_file}\n"
                 f"Add some and save.\n"
                 f"Then press any key to continue...")
        restart(fp=os.path.abspath(__file__), py_executable=sys.executable)

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
    for key in installed_checkers.keys():
        if key in url:
            checker = installed_checkers[key]
            return compare(checker, info)
    print(
        f"Checker for {url} is not found, key is incorrect, or not installed.\n")
    return None


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


def report(results):
    """return True if printed something in terminal else False"""

    printed_once = False
    links = []
    for i, result in enumerate(results, 1):
        if result.is_found():
            links.append(result.current_link)
            if not printed_once:
                print("New update(s)")
                printed_once = True
            print(f"{i}: {result.title} ep {result.current_ep}")
    print()

    cmd = "start "
    if len(links) == 1:
        if wait_key("Press\n'A' to open in browser,\nelse to exit.\n> ", end='').lower() == 'a':
            os.system(cmd + links[0])
    else:
        print("Enter selected number to open via browser,\n'A' to open All,\nelse to exit.")
        while True:
            if len(links) >= 10:
                n = input("> ").strip()
            else:
                n = wait_key("> ", end='').strip().lower()
                print(n)
            # did not open at least one (entered in an exit key)
            if not selectively_open(n, links, cmd):
                break

    return printed_once


def selectively_open(n, links, cmd):
    """" open selected or open all via default browser
        return True if entered 'A', 'a', or a number else False """

    if n == 'a':  # open all
        for link in links:
            os.system(cmd + link)
        return True
    else:  # open selected
        try:
            n = int(n)
        except ValueError:  # entered non-number
            return False
        else:
            try:
                os.system(cmd + links[n - 1])
            except IndexError:  # entered a number but not good
                print(f"Only 1 through {len(links)}, 'A' or else")
                return True  # because entered a number
            else:
                return True


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
