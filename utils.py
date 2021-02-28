import os
import sys

import requests

from exceptions import CannotCheckError

if os.name == 'nt':
    import msvcrt
else:
    import termios

from constants import CONNECTION_ERROR_FLAG, checkers_file, main_file

URLS_FILE = "supported_websites.txt"


def wait_for_internet(prompt="Waiting for internet...", cls=True):
    printed_once = False
    while True:
        try:
            requests.get("https://www.google.com/")
        except requests.exceptions.ConnectionError:
            if prompt and not printed_once:
                print(prompt)
                printed_once = True
        else:
            if cls:
                os.system("cls")
            break


def wait_key(prompt=None, end='\n'):
    """ Wait for a key press on the console and return it as str type. """

    if prompt:
        print(prompt, end=end)

    result = None
    if os.name == 'nt':
        result = msvcrt.getch()
    else:
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result if type(result) == str else result.decode('utf-8')


def see_in_browser(html_text, file="test.html"):
    with open(file, 'w', encoding='utf8') as f:
        f.write(html_text)
    os.system(file)


def install(key, checker_name, url_structure, checker):
    """ install newly defined checker in lab.py to main.py and checkers.py.

    """

    if not (key and checker_name and url_structure):
        print("You need to provide key, checker name, url structure and checker function")
        return False
    if checker_name[-8:] != "_checker":
        print("Invalid checker name (must end with _checker)")
        return False
    from main import INSTALLED_CHECKERS
    if key in INSTALLED_CHECKERS:
        print(f"Found existing key, {key}, already installed")
        return False
    if checker_name in [f.__name__ for f in INSTALLED_CHECKERS.values()]:
        print(
            f"Found existing checker.__name__, {checker_name}, already installed")
        return False
    INSTALLED_CHECKERS[key] = checker
    _install_at_main(key, checker_name, INSTALLED_CHECKERS)
    _install_at_checkers(checker_name, url_structure)
    print(f"Installed {checker_name} with key='{key}' successfully.")
    return True


def _install_at_checkers(checker_name, url_structure):
    """ copies newly defined checker from lab.py to checkers.py (ignore tabbed comments) """

    file = "lab.py"
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()

    first = 0
    last = 0
    for i, line in enumerate(lines):
        if 'def _checker(url="", get_url_struct=False):' in line:
            first = i + 1
        if "return num_ep, last_link" in line:
            last = i + 1
            break
    def_lines = [f'def {checker_name}(url="", get_url_struct=False):\n']
    def_lines.extend(lines[first:last])

    with open(checkers_file, 'r', encoding='utf8') as a:
        codes = a.read()
    with open(checkers_file, 'w', encoding='utf8') as f:
        codes += "\n\n" + ''.join(def_lines)
        f.write(codes)


def _install_at_main(key, checker_name, installed_checkers):

    def create_checker_str(checkers):
        string = "INSTALLED_CHECKERS = {\n"
        for web_key, func in checkers.items():
            if web_key == key:
                string += f'    "{web_key}": {checker_name},\n'
            else:
                string += f'    "{web_key}": {func.__name__},\n'
        string += "}\n"
        return string

    # replace old literal codes with new codes
    with open(main_file, 'r', encoding='utf8') as f:
        lines = f.readlines()
    first_line_index = 0
    last_line_index = 0
    for i, line in enumerate(lines):
        if "INSTALLED_CHECKERS" in line:
            first_line_index = i
        if '}' in line:
            last_line_index = i + 1
            break

    checker_str = create_checker_str(installed_checkers)
    new_code_lines = lines[:first_line_index]
    new_code_lines.append(checker_str)
    new_code_lines.extend(lines[last_line_index:])
    with open(main_file, 'w', encoding='utf8') as f:
        f.writelines(new_code_lines)


def compare(checker, info):
    """
    :param checker: function for each website that returns int(all eps on site), str(link to latest ep)
    :param info: info is read from a line in {gv.info_file}
        info = {
            'url': str,
            'ep': int or None,
            'title': str
        }
    :return: CompareResult if found new ep else None
    """

    try:
        current_ep, current_link = checker(info['url'])
    except requests.exceptions.ConnectionError:
        return CONNECTION_ERROR_FLAG
    except:
        print(
            f"cannot check {info['title']}, ({info['url']}) checker = {checker.__name__}")
        raise CannotCheckError
    else:
        saved_ep = info['ep']
        title = info['title']
        if saved_ep is None:
            return CompareResult(info['url'], title, current_ep)
        else:
            if saved_ep != current_ep:
                return CompareResult(info['url'], title, current_ep, current_link, saved_ep)
            else:
                return None


class CompareResult:
    def __init__(self, url, title, current_ep, current_link=None, old_ep=None):
        self.title = title
        self.current_ep = current_ep
        self.url = url
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

    def __eq__(self, o: object) -> bool:
        if self.__class__.__name__ != o.__class__.__name__:
            return False
        return self.title == o.title

    def __hash__(self) -> int:
        return 123


def get_supported_urls_structures():
    """ return a list of url structures of all supported websites """

    from checkers import __dict__ as d
    urls_structs = []
    for k, v in d.items():
        if "checker" in k and callable(v):
            urls_structs.append(v(get_url_struct=True))
    return urls_structs


def update_url_structs():
    """ write url structures of all supported websites to a text file """

    global URLS_FILE
    with open(URLS_FILE, "w", encoding="utf8") as f:
        urls_structs = get_supported_urls_structures()
        f.write(f"{len(urls_structs)} in total\n")
        for url_struct in urls_structs:
            f.write(f"{url_struct}\n")
    print(f"{URLS_FILE} is updated")


def see_url_structs():
    # code 1 signals something went wrong, could be file not found
    if not os.path.exists(URLS_FILE):
        update_url_structs()
    if os.system("start " + URLS_FILE) == 1:
        print("Something went wrong, woops!")


if __name__ == "__main__":
    pass
