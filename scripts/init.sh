#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

db_ready() {
python << END
import sys
import pymysql.cursors
import os

try:
    connection = pymysql.connect(
        host=os.environ.get('DATABASE_HOST'),
        user=os.environ.get('DATABASE_USER'),
        password=os.environ.get('DATABASE_PASSWORD'),
        db=os.environ.get('DATABASE_NAME'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

    sys.exit(0)

except Exception as e:
    sys.exit(-1)

END
}

echo 'Checking DB connection...'
until db_ready; do
    echo 'Waiting for DB to become available...'
    sleep 1
done
echo 'DB is available'


echo 'Runing Migrations...'
alembic upgrade head

echo 'Starting Server...'
hypercorn app.main:app --reload --bind '0.0.0.0:8000'