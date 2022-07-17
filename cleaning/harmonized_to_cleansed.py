# Here we clean the harmonized data
import pandas as pd
import os, configparser
import sqlite3
import sqlalchemy as sa
import psycopg2
#import json


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__, "..")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

READ_DATA_DIR = config.get("DATA_FOLDER", "Harmonized_Data_Loc")
DB_NAME = config.get("DBS", "DB_Name")
DB_PORT = config.get("DBS", "DB_Port")
SCHEMA_NAME = config.get("DBS", "Cleansed_Schema_Name")
TABLE_NAME = config.get("DBS", "Table_Name")
DB_USER = config.get("CREDENTIALS", "DB_User_Name")
DB_PASS = config.get("CREDENTIALS", "DB_User_Pass")


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


def transform_data(df):
    #print(df)
    return df


def save_to_db_old(data, db_schema, table_name):
    conn = get_connection(db_schema + ".db")
    with conn:
        data.to_sql(name=table_name, con=conn, if_exists="replace", index=False)


def save_to_db(data, db_schema, table_name):
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}"
    engine = sa.create_engine(connection_string, echo=False)
    data.to_sql(name=table_name, schema=db_schema, con=engine, if_exists="replace", index=False)


def run():
    data = read_data(READ_DATA_DIR)
    data = transform_data(data)
    save_to_db(data, SCHEMA_NAME, TABLE_NAME)
