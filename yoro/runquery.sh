#!/bin/bash

echo "running..." >> querylog
DJANGO_SETTINGS_MODULE=yoro.settings python query.py
echo "finished" >> querylog
