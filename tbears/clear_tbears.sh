#!/bin/bash

tbears stop
pkill gunicorn
tbears clear

rm -rf .statedb/ .score/ precommit/
rm -rf ./tbears/*
