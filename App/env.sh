#!/bin/bash
FILE_PATH=${BASH_SOURCE[0]}
DIR_PATH=$(dirname $FILE_PATH)
ABS_DIR_PATH=$(realpath $DIR_PATH)

export PYTHONPATH="$PYTHONPATH:$ABS_DIR_PATH"

if [ -v $PYTHONPATH ]
  then
    export PYTHONPATH="$PYTHONPATH:$ABS_DIR_PATH"
  else
    export PYTHONPATH="$ABS_DIR_PATH"
fi



export DJANGO_SETTINGS_MODULE="noteapp.settings"
