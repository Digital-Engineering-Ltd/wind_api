#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py test
python manage.py spectacular --color --file schema.yml
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:8000