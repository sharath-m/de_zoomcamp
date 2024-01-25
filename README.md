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

```postgresql
-- Q3 Count records
select count(*)
from green_taxi_data
where CAST(lpep_pickup_datetime as DATE) = '2019-09-18';

-- Q4 Largest trip
select CAST(lpep_pickup_datetime as DATE), trip_distance, "PULocationID", "DOLocationID"
from green_taxi_data g
where CAST(lpep_pickup_datetime as DATE) in ('2019-09-18','2019-09-16','2019-09-26','2019-09-21')
ORDER BY trip_distance desc ;

-- Q5 Three biggest pickups
select z."Borough" as borough, count(1) as pickupcount
from green_taxi_data g left join public.zones z on g."PULocationID" = z."LocationID"
group by z."Borough"
order by pickupcount desc;

-- Q6 Largest tip
select g.tip_amount, g."DOLocationID", z."Zone"
from green_taxi_data g LEFT JOIN public.zones z on g."DOLocationID" = z."LocationID"
where g."PULocationID" = 7
order by tip_amount desc

```

### Clean up
```shell
cd week1
docker-compose -f \ docker-compose.yml down --volumes --remove-orphans
```
---

## Week 2
