#!/bin/bash
echo "Enabling virtual environment..."
. venv/bin/activate
echo
echo "Checking project..."
python back-end/manage.py check
echo
echo "Making Migrations..."
python back-end/manage.py makemigrations
echo
echo "Migrating..."
python back-end/manage.py migrate
echo
echo "Collecting static files..."
python back-end/manage.py collectstatic --no-input
echo
echo "Starting back-end in 'localhost:8000'..."
python back-end/manage.py runserver 0.0.0.0:8000 --insecure
echo
