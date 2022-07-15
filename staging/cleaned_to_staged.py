# Here we take the cleansed data and transform it to staged

import pandas as pd

import sqlite3

import os, configparser
#import json


CURR_DIR_PATH = os.path.dirname(os.path.realpath(os.path.join(__file__ ,"..")))

CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/" + CONFIG_NAME)

READ_SCHEMA_NAME = config.get("DBS", "Cleansed_Schema_Name")
WRITE_SCHEMA_NAME = config.get("DBS", "Staged_Schema_Name")
READ_TABLE_NAME = config.get("DBS", "Table_Name")
WRITE_TABLE_NAME = config.get("DBS", "Table_Name")


def get_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
    except sqlite3.Error as e:
        print(e)
    return conn


def read_data(read_schema, read_table):
    conn = get_connection(read_schema + ".db")
    statement = f"SELECT * FROM {read_table}"
    df = pd.read_sql(statement, conn, index_col="index", coerce_float=True, parse_dates=['retrieved', 'datetime'])
    return df


def transform_data(df):
    #print(df)
    return df


def save_to_db(data, db_schema, table_name):
    conn = get_connection(db_schema + ".db")
    with conn:
        data.to_sql(name=table_name, con=conn, if_exists="replace")
        

def run():
    data = read_data(READ_SCHEMA_NAME, READ_TABLE_NAME)
    #print(data)
    data = transform_data(data)
    print(data)
    save_to_db(data, WRITE_SCHEMA_NAME, WRITE_TABLE_NAME)
