import requests
import webbrowser
import time

BASE_URL = 'http://127.0.0.1:5000/'
HEADERS = {'User-Agent': 'TestBot'}

def open_browser(url):
    webbrowser.open(url, new=2)
