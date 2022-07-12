import os, configparser
import json, pprint

import requests

from datetime import datetime

CONFIG_NAME = "config.ini"
CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__ ,"..")))

config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

API_KEY = config.get("DEV", "API_KEY")
BASE_URL = config.get("DEV", "Base_Url")
LATITUDE = config.get("LOCATION", "Latitude")
LONGITUDE = config.get("LOCATION", "Longitude")
DATA_DIR = config.get("DATA_FOLDER", "Raw_Data_Name")


def create_request_string(lat, lon, appid=API_KEY):
    query_str = f"?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={appid}"
    return BASE_URL + query_str

def get_info(lat, lon):
    '''A function that does a request to a URL and 
    returns the resource as a Python dict'''
    req_url = create_request_string(lat, lon, API_KEY)
    resp = requests.get(req_url)
    if resp.status_code == 200:
        return json.loads(resp.text)
    fail_dict = {"response": "Fail!", "Status": resp.status_code}
    return fail_dict

def save_data(dictionary, path):
    '''A function that takes a Python dict and a filepath 
    and saves the dict as a JSON object in that path'''
    file_path = path + "/data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

def source_to_file(lat=LATITUDE, lon=LONGITUDE):
    d = get_info(lat, lon)
    save_data(d, DATA_DIR)
