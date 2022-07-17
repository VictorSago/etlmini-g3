import pandas as pd
from weathers import weather_fio as fio
from weathers import weather_db as wdb


def transform_data(data):
    #print(data)
    df = pd.DataFrame(data)
    return df


def run(read_dir, user, pw, host, port, db_name, schema, table):
    data = fio.read_json_file(read_dir)
    df = transform_data(data)
    wdb.save_to_db(df, user, pw, host, port, db_name, schema, table, replace=True)
