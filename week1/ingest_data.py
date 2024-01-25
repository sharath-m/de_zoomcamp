import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse


def ingest(params):
    user = params.user
    password = params.password
    db_host = params.db_host
    db_port = params.db_port
    db_name = params.db_name
    table_name = params.table_name
    url = params.file_url
    csv_filename = "ingest_file.csv.gz"

    os.system(f"wget {url} -O {csv_filename}")

    engine = create_engine(f"postgresql://{user}:{password}@{db_host}:{db_port}/{db_name}")
    # print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))
    df_iterator = pd.read_csv(csv_filename, iterator=True, chunksize=100000, compression='gzip')
    df = next(df_iterator)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        t_start = time()
        df = next(df_iterator)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()

        print("inserted another chunk, took %.3f second" % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres.')
    # user, password, host, port, database, table name, csv filename

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--db_host', help='postgres host')
    parser.add_argument('--db_port', help='postgres port')
    parser.add_argument('--db_name', help='postgres db name')
    parser.add_argument('--table_name', help='postgres table name')
    parser.add_argument('--file_url', help='csv file url')

    args = parser.parse_args()
    print(args)

    ingest(args)
