#!/bin/bash 
python3 manage.py migrate
rabbitmq-server &
celery -A project worker --loglevel=INFO &
python3 manage.py runserver