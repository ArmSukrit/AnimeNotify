# AnimeNotify
This script checks for new anime episodes on supported websites. Supported websites and url structures of them can be found in checkers.py.

## Usage
- install [python 3.8.6](https://www.python.org/downloads/release/python-386/) or [above](https://www.python.org/downloads/) (or try with your existing python)
- open a new terminal or command prompt and cd to the source code folder

In command prompt, run these
- pip install -r requirements.txt
- python checkers.py -update -see (write url structures to "supported_websites.txt" (-update) and see them (-see))
- python main.py (and read instructions in the console)
- ???
- profit

## Making a new checker for an unsupported website
To write your own checker function, use this draft or see checkers in checkers.py and copy their structures.
```
def anime_example_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "http://anime-example.com/{id}/"  # str(url struct of that website)

    r = requests.get(url, headers=gv.headers)
    # todo: make it return those below
    return None, None  # int(all eps on website), str(link to latest ep)
```
A checker (function) needs to be named {someWeb}_checker needs, takes 2 parameters, url and get_url_struct=False, and returns int(all eps on website), str(link to latest ep) if get_url_struct == False else returns str(url struct of that website). After defining any new checkers in checkers.py, install them at installed_checkers dict in main.py. 

A key of a key/checker_func pair in the dict must be the identifier of that website, for example, for https://www.youtube.com/playlist?list=PLwLSw1_eDZl01_ftoIT3birJWkpxFZkEl, the key could be "youtube" or "youtube.com".
