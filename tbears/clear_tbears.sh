#!/bin/bash

tbears stop
pkill gunicorn
tbears clear

rm -rf .statedb/ .score/ precommit/

find ./tbears -type f -not -name '*.sh' -delete