# Here we take the cleansed data and transform it to staged
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

DB_NAME = config.get("DBS", "DB_Name")
DB_PORT = config.get("DBS", "DB_Port")
READ_SCHEMA_NAME = config.get("DBS", "Cleansed_Schema_Name")
WRITE_SCHEMA_NAME = config.get("DBS", "Staged_Schema_Name")
READ_TABLE_NAME = config.get("DBS", "Table_Name")
WRITE_TABLE_NAME = config.get("DBS", "Table_Name")
DB_USER = config.get("CREDENTIALS", "DB_User_Name")
DB_PASS = config.get("CREDENTIALS", "DB_User_Pass")


def get_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
    except sqlite3.Error as e:
        print(e)
    return conn


def read_data_sqlite(read_schema, read_table):
    conn = get_connection(read_schema + ".db")
    statement = f"SELECT * FROM {read_table}"
    df = pd.read_sql(statement, conn, index_col=None, coerce_float=True, parse_dates=['retrieved', 'datetime'])
    return df


def read_data(read_schema, read_table):
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}"
    engine = sa.create_engine(connection_string, echo=False)
    statement = f"SELECT * FROM {read_schema}.{read_table}"
    df = pd.read_sql(statement, engine, index_col=None, coerce_float=True, parse_dates=['retrieved', 'datetime'])
    return df


def transform_data(df):
    return df


def save_to_db_sqlite(data, db_schema, table_name):
    conn = get_connection(db_schema + ".db")
    with conn:
        data.to_sql(name=table_name, con=conn, if_exists="append", index=False)


def save_to_db(data, db_schema, table_name):
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}"
    engine = sa.create_engine(connection_string, echo=False)
    data.to_sql(name=table_name, schema=db_schema, con=engine, if_exists="replace", index=False)


def run():
    data = read_data(READ_SCHEMA_NAME, READ_TABLE_NAME)
    #print(data)
    data = transform_data(data)
    save_to_db(data, WRITE_SCHEMA_NAME, WRITE_TABLE_NAME)
