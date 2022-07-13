# Take the extracted raw data and save it to data/harmonized

import os, configparser
import json
import pprint

from datetime import datetime


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__ ,"..")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

READ_DATA_DIR = config.get("DATA_FOLDER", "Raw_Data_Loc")
WRITE_DATA_DIR = config.get("DATA_FOLDER", "Harmonized_Data_Loc")

def read_data(path):
    file_path = path + "/data.json"
    with open(file_path, "r") as f:
        raw_data = json.load(f)
    #print(type(raw_data))
    return raw_data

def transform_json_data(data):
    dates = []
    temps = []
    pressures = []
    pops = []
    #precipitations = []
    for hour in data["hourly"]:
        dates.append(datetime.utcfromtimestamp(hour["dt"]))
        temps.append(hour["temp"])
        pressures.append(hour["pressure"])
        pops.append(round(hour["pop"] * 100, 1))            # Probabilities of precipitation
    #print(type(raw_data["hourly"]))
    result = {"date" : dates, "temperature": temps, "air_pressure": pressures}
    result["probablities_of_precipitation"] = pops
    return result

def save_to_file(filepath, data):
    pprint.pprint(data)

def run():
    raw = read_data(CURR_DIR_PATH + "/" + READ_DATA_DIR)
    harmonized = transform_json_data(raw)
    save_to_file(CURR_DIR_PATH + "/" + WRITE_DATA_DIR, harmonized)