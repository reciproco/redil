#!/bin/bash

source $APP_DIR/env/env.sh

cd $APP_DIR

source $APP_DIR/venv/bin/activate

echo "starting worker $APP_NAME in $APP_DIR as `whoami`"

python worker.py
