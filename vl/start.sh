#!/usr/bin/env bash

service nginx start
uwsgi --ini swagger_server/uwsgi.ini
