from weathers import weather_db as wdb


def transform_data(df):
    return df


def run(user, pw, host, port, db, read_schema, write_schema, read_table, write_table):
    data = wdb.read_from_db(user, pw, host, port, db, read_schema, read_table)
    data = transform_data(data)
    wdb.save_to_db(data, user, pw, host, port, db, write_schema, write_table)
