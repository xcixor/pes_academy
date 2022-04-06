#!/bin/sh
redis-server /etc/redis/redis.conf protected-mode no
# test redis
redis-cli -h localhost -p 6379 ping
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn -b 0.0.0.0:8000 core.wsgi:application --timeout 90
exec "$@"