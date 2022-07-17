import pandas as pd
import sqlalchemy as sa
import psycopg2


def read_from_db(user, pw, host, port, db_name, db_schema, table_name):
    connection_string = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db_name}"
    engine = sa.create_engine(connection_string, echo=False)
    statement = f"SELECT * FROM {db_schema}.{table_name}"
    df = pd.read_sql(statement, engine, index_col=None, coerce_float=True, parse_dates=['retrieved', 'forecast_dt'])
    return df


def save_to_db(data, user, pw, host, port, db_name, db_schema, table_name, replace=False):
    connection_string = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db_name}"
    engine = sa.create_engine(connection_string, echo=False)
    method = "replace" if replace else "append"
    data.to_sql(name=table_name, schema=db_schema, con=engine, if_exists=method, index=False)
