#!/bin/bash

tbears stop
pkill gunicorn
tbears start -c ./config/localhost/tbears_server_config.json
