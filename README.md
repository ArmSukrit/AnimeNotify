# AnimeNotify
  This script checks for new anime episodes on supported websites. Supported websites and url structures of them can be found in checkers.py.
  
## Usage
- install [python 3.8.6](https://www.python.org/downloads/release/python-386/) or [above](https://www.python.org/downloads/)
- open a new terminal or command prompt and cd to the source code folder

In command prompt, run these
- pip install -r requirements.txt
- python main.py (and read instructions in the console)
- ???
- profit

note: all supported sites can be seen in checkers.py

## Making a new checker for an unsupported website
To write your own checker function, first, you should see checkers.py. Each checker needs to return int(all eps on website), str(link to latest ep). After defining any new functions in checkers.py, install them at installed_checkers dict in main.py. 

A key of a key/checker_func pair in the dict must be the identifier of that website, for example, for https://www.youtube.com/playlist?list=PLwLSw1_eDZl01_ftoIT3birJWkpxFZkEl, the key could be "youtube" or "youtube.com".
