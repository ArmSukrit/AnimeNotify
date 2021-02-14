# AnimeNotify
This script checks for new anime episodes on supported websites. If it detects new episodes, a clickable GUI, implemented with Kivy, is launched.

## Download
- download a zip version [here](https://github.com/ArmSukrit/AnimeNotify/archive/master.zip) and extract all to an empty folder  
or clone https://github.com/ArmSukrit/AnimeNotify.git
- install [python 3.8.6](https://www.python.org/downloads/release/python-386/) or [above](https://www.python.org/downloads/) (or try with your existing python)
## Usage
open a command prompt or equivalent, and run these  
for first time use
- pip install -r requirements.txt
- python main.py
- ???
- profit

execute add.py to add more urls and titles  
execute checkers.py to see all supported websitess  
open urls.csv to see all saved urls and titles

## More profit
You can make a batch file (.bat) for an **esay double click method to run**
- open a text editor and paste these
```
python "...\path\to\main.py"
```
- save as animenotify.bat
- double click on it (same thing with open cmd and execute "python main.py" above)
- ???
- more profit

note: "...\path\to\main.py" is the full path of main.py, for example, "C:\Users\Admin\Downloads\AnimeNotify-master\main.py"

## Making a new checker for an unsupported website
Every checker in checkers.py is a fucntion that 
- needs to be named {someWeb}_checker
- takes 2 parameters, url="" and get_url_struct=False
- returns str(url struct of that website) if get_url_struct == True  
else returns int(all eps on website), str(link to latest ep)

To write your own checker function, copy the code below and paste into a new file named "lab.py" in the same directory as main.py and checkers.py.  
Redefine the _checker function to return values correctly based of url and get_url_struct.
```
# in lab.py

from utils import install
import constants
import requests


def _checker(url="", get_url_struct=False):
    if get_url_struct:
        # str(url struct of that website)
        return "http://anime-example.com/{id}/"

    # r = requests.get(url, headers=constants.headers)
    # todo: make it return those below

    num_ep = 10
    last_link = "http://anime-example.com/{id}/ep10"
    # return int(all eps on website), str(link to latest ep)
    return num_ep, last_link  # do not change


def test(url):
    try:
        print(_checker(url))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # print the result of your checker
    test(url="http://anime-example.com/543/")

    # fill these three below before installation
    key = "anime-example"  # identifier of the website
    # valid function name (ends with _checker)
    checker_name = "anime_example_checker"
    # url structure when copied from address bar
    # conventional struct elements: {id}, {title}, {ep}, {year}, {month}, ...
    url_structure = "http://anime-example.com/{id}/"

    # comment/uncomment below to install (will write to main.py and checkers.py directly)
    # install(key, checker_name, url_structure, _checker)

```
After finishing writing the body of your checker, you can test your checker by calling test(url="your_url"). After sucessfull testing, fill in key, checker_name, and url_structure, then uncomment and call install() below.

The key must be the identifier of the website, for example
- for http://anime-example.com/{id}/, the key could be "anime-example" or "anime-example.com"
- for https://www.youtube.com/playlist?list=PLwLSw1_eDZl01_ftoIT3birJWkpxFZkEl, the key could be "youtube" or "youtube.com".
