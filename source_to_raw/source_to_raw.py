import os
import requests
import json, pprint


#CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BASE_URL = "https://swapi.dev/api/"

def get_info(section, searchterm):
    req_url = BASE_URL + section + "/" + searchterm
    resp = requests.get(req_url)
    return resp.json()

