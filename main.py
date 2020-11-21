import os
import csv
import concurrent.futures


from checkers import *
checkers = {
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
}
import global_var as gv


def main():
    # read urls from csv
    data = read_info(gv.info_file)

    # check each url using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check, data)


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
            checkers[key](info)
            break


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
