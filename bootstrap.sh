#!/bin/bash

source $APP_DIR/env/env.sh

cd $APP_DIR

source $APP_DIR/venv/bin/activate

echo "starting $APP_NAME in $APP_DIR as `whoami`"

exec $APP_DIR/venv/bin/gunicorn wsgi:app \
  --name $APP_NAME \
  --workers 2 \
  --bind localhost:$APP_PORT \
  --logfile=-



