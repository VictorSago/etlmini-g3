import json
import requests
from weathers import weather_fio as fio


def get_city_from_coords(api_url, lat, lon, api_key):
    query_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    resp = requests.get(api_url, query_params)
    if resp.status_code not in [200]:
        fail_dict = {"city_response": "Fail!", "Status": resp.status_code}
        return fail_dict
    geo_pos = json.loads(resp.text)
    city_data = {"city": geo_pos[0]["name"],
                 "country": geo_pos[0]["country"],
                 "city_lat": geo_pos[0]["lat"],
                 "city_lon": geo_pos[0]["lon"]}
    return city_data


def get_weather_from_coords(api_url, lat, lon, api_key):
    query_params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,alerts",
        "units": "metric",
        "appid": api_key
    }
    resp = requests.get(api_url, query_params)
    if resp.status_code not in [200]:
        fail_dict = {"weather_response": "Fail!", "Status": resp.status_code}
        return fail_dict
    return json.loads(resp.text)


def get_info(weather_url, geo_url, lat, lon, api_key):
    """A function that does a request to a URL and
    returns the resource as a Python dict"""
    weather_data = get_weather_from_coords(weather_url, lat, lon, api_key)
    location_data = get_city_from_coords(geo_url, lat, lon, api_key)
    location_data.update(weather_data)
    return location_data


def source_to_file(weather_url, geo_url, lat, lon, api_key, save_dir):
    d = get_info(weather_url, geo_url, lat, lon, api_key)
    fio.save_json_file(d, save_dir)
