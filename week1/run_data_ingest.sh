/usr/bin/env bash

echo "${USER}"
echo "${DB_HOST}"
echo "${TABLE_NAME}"
echo "${FILE_URL}"
echo "${ZONE_URL}"

python ingest_data_improved.py \
        --user="${USER}" \
        --password="${PASSWORD}" \
        --db_host="${DB_HOST}" \
        --db_port="${DB_PORT}" \
        --db_name="${DB_NAME}" \
        --table_name="${TABLE_NAME}" \
        --file_url="${FILE_URL}" \
        --zone_url="${ZONE_URL}"
