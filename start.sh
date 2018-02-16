#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn...
exec gunicorn event_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --timeout 600 \
    --log-level=debug \
    --access-logfile - \
