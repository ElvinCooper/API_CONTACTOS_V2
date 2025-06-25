#!/bin/bash

if [ "$FLASK_ENV" = "development" ]; then
    echo "Correr el entorno de desarrollo con auto-reload"
    flask run --host=0.0.0.0 --port=8000 --reload
else
    echo "Correr el entorno de desarrollo con Gunicorn"
    gunicorn -b 0.0.0.0:8000 "app:create_app()"
fi
