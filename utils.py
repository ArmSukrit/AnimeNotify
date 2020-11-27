import sys
import os
import requests
import msvcrt
import termios


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


def wait_key(prompt=None):
    """ Wait for a key press on the console and return it. """

    if prompt:
        print(prompt)

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

    return result