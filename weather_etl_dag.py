from airflow import DAG
from airflow.operators.python import PythonOperator

import os
import configparser
from datetime import datetime

from weather_etl.weathers import weather_ex as wex
from weather_etl.weathers import weather_har as har
from weather_etl.weathers import weather_cln as cln
from weather_etl.weathers import weather_stg as stg


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__, "")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

API_KEY = config.get("DEV", "API_KEY")
BASE_URL = config.get("URLS", "Base_Url")
GEO_URL = config.get("URLS", "Reverse_Geo_Url")
LATITUDE = config.get("LOCATION", "Latitude")
LONGITUDE = config.get("LOCATION", "Longitude")
RAW_DATA_DIR = config.get("DATA_FOLDER", "Raw_Data_Loc")
HAR_DATA_DIR = config.get("DATA_FOLDER", "Harmonized_Data_Loc")
DB_NAME = config.get("DBS", "DB_Name")
DB_PORT = config.get("DBS", "DB_Port")
CLEANSED_SCHEMA_NAME = config.get("DBS", "Cleansed_Schema_Name")
STAGED_SCHEMA_NAME = config.get("DBS", "Staged_Schema_Name")
CLEANSED_TABLE_NAME = config.get("DBS", "Table_Name")
STAGED_TABLE_NAME = config.get("DBS", "Table_Name")
DB_USER = config.get("CREDENTIALS", "DB_User_Name")
DB_PASS = config.get("CREDENTIALS", "DB_User_Pass")


def _get_weather_data(lat=LATITUDE, lon=LONGITUDE):
    extraction_params = {
        "weather_url": BASE_URL,
        "geo_url": GEO_URL,
        "lat": lat,
        "lon": lon,
        "api_key": API_KEY,
        "save_dir": RAW_DATA_DIR
    }
    wex.source_to_file(**extraction_params)


def _harmonize_data():
    har.run(RAW_DATA_DIR, HAR_DATA_DIR)


def _cleanse_data():
    cleaning_params = {
        "read_dir": HAR_DATA_DIR,
        "user": DB_USER,
        "pw": DB_PASS,
        "host": "localhost",
        "port": DB_PORT,
        "db_name": DB_NAME,
        "schema": CLEANSED_SCHEMA_NAME,
        "table": CLEANSED_TABLE_NAME
    }
    cln.run(**cleaning_params)


def _stage_data():
    staging_params = {
        "user": DB_USER,
        "pw": DB_PASS,
        "host": "localhost",
        "port": DB_PORT,
        "db": DB_NAME,
        "read_schema": CLEANSED_SCHEMA_NAME,
        "write_schema": STAGED_SCHEMA_NAME,
        "read_table": CLEANSED_TABLE_NAME,
        "write_table": STAGED_TABLE_NAME
    }
    stg.run(**staging_params)


with DAG("weather_etl_dag", start_date=datetime(2022, 7, 1), schedule_interval="@hourly", catchup=False) as dag:
    source_to_raw = PythonOperator(
        task_id="get_weather",
        python_callable=_get_weather_data,
    )

    raw_to_harmonized = PythonOperator(
        task_id="harmonize",
        python_callable=_harmonize_data
    )

    harmonized_to_cleansed = PythonOperator(
        task_id="cleanse",
        python_callable=_cleanse_data
    )

    cleansed_to_staged = PythonOperator(
        task_id="stage",
        python_callable=_stage_data
    )

    source_to_raw >> raw_to_harmonized >> harmonized_to_cleansed >> cleansed_to_staged
