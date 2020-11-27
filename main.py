import concurrent.futures
import csv
import os
import sys
from time import sleep

import global_var as gv
from utils import wait_for_internet, wait_key, restart
from checkers import anime_hayai_checker, four_anime_to_checker, kissanimes_tv_checker, youtube_playlist_checker, \
    crunchyroll_checker, anime_master_checker, anime_sugoi_checker

# each key of checkers dict is something common across urls from the same website
installed_checkers = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
    "kissanimes.tv": kissanimes_tv_checker,
    "youtube": youtube_playlist_checker,
    "crunchyroll": crunchyroll_checker,
    "anime-master": anime_master_checker,
    "anime-sugoi": anime_sugoi_checker,
}


def main():
    wait_for_internet()

    # read urls from csv
    data, duplicate_urls = read_info(gv.info_file)
    print_what_to_check(data)
    if duplicate_urls:
        report_duplicates(duplicate_urls)

    # check each url using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [result for result in executor.map(check, data) if result is not None]

    # results is a list of CompareResult(s)
    if results:
        save(results)
        report(results)
        wait_key("Press any key to exit...")
    else:
        print("No update is found.")
        sleep(3)


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
        wait_key(f"Add url to {gv.info_file} and save.\n"
                 f"Press any key to continue...")
        restart(fp=os.path.abspath(__file__), py_executable=sys.executable)
        exit(0)

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
                 f"Press any key to continue...")
        restart(fp=os.path.abspath(__file__), py_executable=sys.executable)
        exit(0)

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
    :return: checkers.CompareResult if found new ep else None
    """

    url = info['url']
    for key in installed_checkers.keys():
        if key in url:
            return installed_checkers[key](info)  # call a specific checker based on key
    print(f"cannot find any key that matches with {url}.\n"
          f"make sure to install the checker for this website. See installed_checkers in main.py\n")
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
                        line = ','.join(components[:2]) + ',' + str(result.current_ep)  # replace old ep with new ep
                    else:
                        added = True
                        if line[-1] != ',':
                            line += ','
                        line += str(result.current_ep)
                        print(f"added '{result.title}' to checklist. (current ep {result.current_ep})")
                    line += '\n'
                    break
            f.write(line)
        if added:
            print()
        return added


def report(results):
    """return True if printed something in terminal else False"""

    printed_once = False
    for result in results:
        if result.is_found():
            if not printed_once:
                print("New update(s)")
                printed_once = True
            print(f"- {result.title}, ep {result.current_ep}, {result.current_link}")
    if printed_once:
        print()
    return printed_once


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
