#!/usr/bin/env bash
# wait-for-it.sh

until pg_isready -h "$POSTGRES_HOST"; do
	echo "Postgres is unavailable - sleeping"
	sleep 1
done

echo "Postgres is up - executing command"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

if [ "$DEBUG" = "False" ]; then
	echo "Starting: production mode"
	gunicorn --bind 0.0.0.0:8000 estoque.wsgi:application
else
	echo "Starting: development mode"
	python manage.py runserver 0.0.0.0:8000
fi


