# Here we clean the harmonized data

from unicodedata import name
import pandas as pd

import sqlite3

import os, configparser
import json


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__ ,"..")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

READ_DATA_DIR = config.get("DATA_FOLDER", "Harmonized_Data_Loc")


def get_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
    except sqlite3.Error as e:
        print(e)
    return conn



def read_data(filepath):
    file_path = filepath + "/data.json"
    df = pd.read_json(file_path)
    return df


def transform_data(df, db_file):
    #print(df)
    return df

def save_to_db(data, db_schema="cleansed", table_name="weather_data"):
    conn = get_connection(db_schema + ".db")
    
    with conn:
        data.to_sql(name=table_name, con=conn, if_exists="replace")
        

def run():
    data = read_data(READ_DATA_DIR)
    data = transform_data(data, "cleansed.db")
    save_to_db(data)
