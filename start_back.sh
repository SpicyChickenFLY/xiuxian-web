#!/bin/bash

WORKSPACE=$(dirname $(readlink -f "$0"))

cd $WORKSPACE/back
/mnt/Mine/Code/python/venv/bin/python app.py
