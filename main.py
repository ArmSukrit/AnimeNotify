import os
import csv
import concurrent.futures
from time import sleep
import requests


from checkers import anime_hayai_checker, four_anime_to_checker
# each key of checkers dict is something common across urls from the same website
checkers = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
}
import global_var as gv


def main():
    wait_for_internet()

    # read urls from csv
    data = read_info(gv.info_file)
    print_what_to_check(data)

    # check each url using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [result for result in executor.map(check, data) if result is not None]

    # results is a list of CompareResult(s)
    if results:
        save(results)
        if report(results):
            input()  # to not terminate the terminal instantly
    else:
        print("No update is found.")
        sleep(3)


def print_what_to_check(data):
    print("Checking...")
    for each in data:
        print(f"- {each['title']}  ({each['url']})")
    print("_________________________________________________________________________________________________________\n")


def wait_for_internet():
    printed_once = False
    while True:
        try:
            requests.get("https://www.google.com/")
        except requests.exceptions.ConnectionError:
            if not printed_once:
                print("Waiting for internet...")
                printed_once = True
        else:
            os.system("cls")
            break


def read_info(file):
    """return list[dict], keys in dict are url, ep, title"""

    def create_csv_if_not_exist(path):
        if not os.path.exists(path):
            with open(path, 'w') as new_file:
                new_file.write(','.join(gv.field_names) + '\n')
            return True
        return False

    if create_csv_if_not_exist(file):
        input(f"exit program and add url into {gv.info_file}\n"
              f"then rerun this program (do not forget to save the file)")
        exit(0)

    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=gv.field_names)
        next(reader)
        data = []
        for line in reader:
            data.append({
                "url": line['url'],
                'ep': int(line['ep']) if line['ep'] else None,
                'title': line['title']
            })
    return data


def check(info):
    """
    :param info: list of dict
    :return: checkers.CompareResult if found new ep else None
    """
    url = info['url']
    for key in checkers.keys():
        if key in url:
            return checkers[key](info)  # call a specific checker based on key


def save(results, file=gv.info_file):
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            for result in results:
                if result.title in line:
                    line = line.rstrip()
                    if result.old_ep:
                        components = line.split(',')
                        line = ','.join(components[:2]) + ',' + str(result.current_ep)  # replace old ep with new ep
                    else:
                        line += str(result.current_ep)
                    line += '\n'
                    break
            f.write(line)


def report(results):
    """return True if printed something in terminal else False"""
    printed_once = False
    reported = False
    for result in results:
        if result.is_found():
            if not printed_once:
                print("New update(s)")
                printed_once = True
            print(f"- {result.title}, ep {result.current_ep}, {result.current_link}")
            reported = True
    return reported


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
