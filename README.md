## Week 1

### Bring up services - postgres, pgadmin, python/panda
The credentials and program inputs are read from git ignored, `yellow.env` or `green.env` files

### green.env entries
```
user=
password=
pgadmin_user=pgadmin@pgsql.com
pgadmin_password=
db_host=postgres
db_port=5432
db_name=ny_taxi
table_name=green_taxi_data
file_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
zone_url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
```

### Download and ingest data into postgres
```shell
cd week1
docker-compose -f \ docker-compose.yml --env-file=green.env up -d --build
```

### Clean up
```shell
cd week1
docker-compose -f \ docker-compose.yml down --volumes --remove-orphans
```
---

## Week 2
