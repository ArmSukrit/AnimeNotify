import sys
import os
import requests
import sys


def wait_for_internet(prompt=None):
    printed_once = False
    while True:
        try:
            requests.get("https://www.google.com/")
        except requests.exceptions.ConnectionError:
            if prompt:
                if not printed_once:
                    print(prompt)
                    printed_once = True
        else:
            os.system("cls")
            break


def wait_key(prompt=None, end='\n'):
    """ Wait for a key press on the console and return it. """

    if prompt:
        print(prompt, end=end)

    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
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

    return result


def see_in_browser(html_text, file="test.html"):
    with open(file, 'w', encoding='utf8') as f:
        f.write(html_text)
    os.system(file)


def restart(fp, py_executable="python"):
    """restart the caller python script of this func"""
    os.system(f"{py_executable} {fp}")
