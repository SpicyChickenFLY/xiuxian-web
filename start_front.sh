#!/bin/bash

WORKSPACE=$(dirname $(readlink -f "$0"))

cd $WORKSPACE/front
npm run dev
