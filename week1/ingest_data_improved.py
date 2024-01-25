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
    yellow_taxi_data_url = params.file_url
    yellow_taxi_data_csv_filename = "ingest_yellow_taxi_data.csv.gz"
    zone_data_url = params.zone_url
    zone_csv_filename = "zone_file.csv"

    os.system(f"wget {yellow_taxi_data_url} -O {yellow_taxi_data_csv_filename}")
    os.system(f"wget {zone_data_url} -O {zone_csv_filename}")

    engine = create_engine(f"postgresql://{user}:{password}@{db_host}:{db_port}/{db_name}")

    ingest_table(engine, table_name, source_csv_file=yellow_taxi_data_csv_filename, enrich_column=True, compression='gzip')
    ingest_table(engine, table_name="zones", source_csv_file=zone_csv_filename, enrich_column=False)


def ingest_table(engine, table_name, source_csv_file, enrich_column, compression=None):

    df_iterator = pd.read_csv(source_csv_file, compression=compression, chunksize=100000)
    for i, df_chunk in enumerate(df_iterator):
        t_start = time()
        # if enrich_column:
        #     df_chunk.tpep_pickup_datetime = pd.to_datetime(df_chunk.tpep_pickup_datetime)
        #     df_chunk.tpep_dropoff_datetime = pd.to_datetime(df_chunk.tpep_dropoff_datetime)
        if enrich_column:
            df_chunk.lpep_pickup_datetime = pd.to_datetime(df_chunk.lpep_pickup_datetime)
            df_chunk.lpep_dropoff_datetime = pd.to_datetime(df_chunk.lpep_dropoff_datetime)

        if i == 0:
            # create the table
            df_chunk.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()

        print(f"inserted another chunk of {table_name} data, took %.3f second {t_end - t_start}")


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
    parser.add_argument('--zone_url', help='zone csv file url')

    args = parser.parse_args()
    print(args)

    ingest(args)
