#!/usr/bin/env bash

service nginx start
redis-server &
uwsgi --ini uwsgi.ini
