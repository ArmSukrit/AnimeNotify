import os
import csv
import concurrent.futures


from checkers import *
# each key of checkers dict is something common across urls from the same website
checkers = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
}
import global_var as gv


def main():
    # read urls from csv
    data = read_info(gv.info_file)
    print_what_to_check(data)

    # check each url using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("New update(s), if there is")
        if True in executor.map(check, data):
            input()  # to not terminate program instantly


def print_what_to_check(data):
    print("Checking...")
    for each in data:
        print(f"- {each['title']}  ({each['url']})")
    print("_________________________________________________________________________________________________________\n")


def read_info(file):
    """return list[dict], keys in dict are url, ep, title"""
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
            # print(data)
    return data


def check(info):
    url = info['url']
    for key in checkers.keys():
        if key in url:
            if checkers[key](info):
                return True
            else:
                return False


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
