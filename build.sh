#!/usr/bin/env sh

set -e

echo "Running migrations"
python3 manage.py migrate --noinput

python3 manage.py qcluster &

uwsgi --http "0.0.0.0:${PORT}" --single-interpreter --module app.wsgi --master --processes 4 --threads 2