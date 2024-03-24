#!/bin/bash

FAILURE_CODE=1
MIN_ARGS_COUNT=3

if [[ $# < $MIN_ARGS_COUNT ]]; then
  printf "Not enough arguments\n"
  exit $FAILURE_CODE
fi

SRC_PATH="$1"
DST_PATH="$2"
HOST_PASS="$3"

last_modification_date=$(stat --format="%y" "$SRC_PATH")
while [ true ]; do
  modification_date=$(stat --format="%y" "$SRC_PATH")
  if [[ "$modification_date" > "$last_modification_date" ]]; then
    printf "File has been modified: %s -> %s\n" \
      "$last_modification_date" \
      "$modification_date"
    printf "Sending modification over scp\n"
    sshpass -p "$HOST_PASS" scp "$SRC_PATH" "$DST_PATH"
    last_modification_date="$modification_date"
  fi
  sleep 0.5s
done
