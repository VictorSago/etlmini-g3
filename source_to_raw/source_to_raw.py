import os
import requests
import json, pprint


#CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BASE_URL = "https://swapi.dev/api/"

def get_info(section, searchterm):
    req_url = BASE_URL + section + "/" + searchterm
    resp = requests.get(req_url)
    if resp.status_code == 200:
        return json.loads(resp.text)
    return f"Fail! Response code: {resp.status_code}"

