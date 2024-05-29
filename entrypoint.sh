#!/bin/bash

# Collect static files
# echo "Collect static files"
# poetry run python manage.py collectstatic --noinput

# # Apply database migrations
# echo "Apply makemigrations "
poetry run python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
poetry run python manage.py migrate

# Apply  fixture load
echo "Apply  fixture load"
poetry run python manage.py loaddata users.json


# Start server
echo "Starting server"
poetry run python manage.py runserver 0.0.0.0:8000