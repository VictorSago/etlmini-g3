import os, configparser
import json
import requests
# import pprint
# from datetime import datetime


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__, "..")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

API_KEY = config.get("DEV", "API_KEY")
BASE_URL = config.get("URLS", "Base_Url")
GEO_URL = config.get("URLS", "Reverse_Geo_Url")
LATITUDE = config.get("LOCATION", "Latitude")
LONGITUDE = config.get("LOCATION", "Longitude")
DATA_DIR = config.get("DATA_FOLDER", "Raw_Data_Loc")


def create_request_string(lat, lon, appid=API_KEY):
    query_str = f"?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={appid}"
    return BASE_URL + query_str


def get_city_from_coords(lat, lon, api_key):
    query_par = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    resp = requests.get(GEO_URL, query_par)
    if resp.status_code not in [200]:
        fail_dict = {"city_response": "Fail!", "Status": resp.status_code}
        return fail_dict
    geo_pos = json.loads(resp.text)
    city_data = {"city": geo_pos[0]["name"],
                 "country": geo_pos[0]["country"],
                 "city_lat": geo_pos[0]["lat"],
                 "city_lon": geo_pos[0]["lon"]}
    return city_data


def get_weather_from_coords(lat, lon, api_key):
    query_par = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,alerts",
        "units": "metric",
        "appid": api_key
    }
    resp = requests.get(BASE_URL, query_par)
    if resp.status_code not in [200]:
        fail_dict = {"weather_response": "Fail!", "Status": resp.status_code}
        return fail_dict
    return json.loads(resp.text)


def get_info(lat, lon, api_key):
    """A function that does a request to a URL and
    returns the resource as a Python dict"""
    # req_url = create_request_string(lat, lon, API_KEY)
    weather_data = get_weather_from_coords(lat, lon, api_key)
    location_data = get_city_from_coords(lat, lon, api_key)
    # print(weather_data)
    location_data.update(weather_data)
    return location_data


def save_data(dictionary, path):
    """A function that takes a Python dict and a filepath
    and saves the dict as a JSON object in that path"""
    file_path = path + "/data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


def source_to_file(lat=LATITUDE, lon=LONGITUDE, api_key=API_KEY):
    d = get_info(lat, lon, api_key)
    save_data(d, DATA_DIR)
