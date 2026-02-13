#!/bin/bash

export MODULE_NAME="app.asgi"
export VARIABLE_NAME="application"
export HOST="0.0.0.0"
export PORT=80

python manage.py collectstatic

python manage.py makemigrations
python manage.py migrate

python manage.py create_superuser
python manage.py create_default_stripe_product_and_price_ids

if [ "$UVICORN_RELOAD" = "true" ]; then
    uvicorn $MODULE_NAME:$VARIABLE_NAME --host $HOST --port $PORT --reload --reload-include '*.*'
else
    uvicorn $MODULE_NAME:$VARIABLE_NAME --host $HOST --port $PORT
fi