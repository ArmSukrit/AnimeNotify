# AnimeNotify
This script checks for new anime episodes on supported websites. If it detects new episodes, a clickable GUI, implemented with Kivy, is launched.

## Download
- download a zip version [here](https://github.com/ArmSukrit/AnimeNotify/archive/master.zip) and extract all to an empty folder  
or clone https://github.com/ArmSukrit/AnimeNotify.git
- install [python 3.8.6](https://www.python.org/downloads/release/python-386/) or [above](https://www.python.org/downloads/) (or try with your existing python)
## Usage
open a command prompt or equivalent, and run these
- pip install -r requirements.txt
- python main.py
- ???
- profit

## More profit
You can make a batch file (.bat) for an **esay double click method to run**
- open a text editor and paste these
```
python "...\path\to\main.py"
```
- save as animenotify.bat
- double click on it (same thing with open cmd and execute python main.py)
- ???
- more profit

note: "...\path\to\main.py" is the full path of main.py, for example, "C:\Users\Admin\Downloads\AnimeNotify-master\main.py"

## Making a new checker for an unsupported website
To write your own checker function, use this draft and define it in checkers.py.
```
# checkers.py

def anime_example_checker(url="", get_url_struct=False):
    if get_url_struct:
        return "http://anime-example.com/{id}/"  # str(url struct of that website)

    r = requests.get(url, headers=gv.headers)
    # todo: make it return those below
    return 10, "http://anime-example.com/{id}/ep10"  # int(all eps on website), str(link to latest ep)
```
A checker (function) needs to be named {someWeb}_checker, takes 2 parameters, url and get_url_struct=False, and returns int(all eps on website), str(link to latest ep) if get_url_struct == False else returns str(url struct of that website). 

After defining any new checkers in checkers.py, install them at INSTALLED_CHECKERS dict in main.py. 
```
# main.py

from checkers import *
...

INSTALLED_CHECKERS = {
    "anime-example": anime_example_checker,  # don't forget to install here!
    "anime-hayai": anime_hayai_checker,
    "4anime.to": four_anime_to_checker,
    ...
}
```
A key of a key/checker_func pair in the dict must be the identifier of that website, for example
- for http://anime-example.com/{id}/, the key could be "anime-example" or "anime-example.com"
- for https://www.youtube.com/playlist?list=PLwLSw1_eDZl01_ftoIT3birJWkpxFZkEl, the key could be "youtube" or "youtube.com".
