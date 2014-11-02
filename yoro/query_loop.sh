#!/bin/bash

function exit() {
  exit
}

trap exit SIGHUP SIGINT SIGTERM

while true; do
  ./runquery.sh
  sleep 10
done
