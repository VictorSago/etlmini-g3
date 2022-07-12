import os, configparser
import json, pprint

import requests

from datetime import datetime

CONFIG_NAME = "config.ini"
CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__ ,"..")))

print("current dir path:", CURR_DIR_PATH)
print("Config File:", CURR_DIR_PATH + "/" + CONFIG_NAME)

BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"

config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

API_KEY = config.get("DEV", "API_KEY")
latitude = config.get("LOCATION", "Latitude")
longitude = config.get("LOCATION", "Longitude")
data_folder = config.get("DATA_FOLDER", "Raw_Data_Name")


def create_request_string(lat=latitude, lon=longitude, appid=API_KEY):
    query_str = f"?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={appid}"
    return BASE_URL + query_str

def get_info(lat, lon):
    '''a function that does a request to a URL and 
    returns the resource as a Python dict'''
    req_url = create_request_string(lat, lon, API_KEY)
    resp = requests.get(req_url)
    if resp.status_code == 200:
        return json.loads(resp.text)
    fail_dict = {"response": "Fail!", "Status": resp.status_code}
    return fail_dict

# def save_data2(dictionary, path):
#     '''A function that takes a Python dict and a filepath 
#     and saves the dict as a JSON object in that path'''
#     #print(os.getcwd())
#     file_path = path + "/data.json"
#     with open(file_path, "w") as f:
#         lines = []
#         lines.append("{")
#         for key, value in dictionary.items():
#             line = '"' + key + ': ' + str(value) + "\n"
#             lines.append()
#         lines.append("}")
#         f.writelines(lines)

def save_data(dictionary, path):
    '''A function that takes a Python dict and a filepath 
    and saves the dict as a JSON object in that path'''
    file_path = path + "/data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

def source_to_file(searchstring):
    d = get_info(searchstring)
    save_data(d, "data/testing/raw")
