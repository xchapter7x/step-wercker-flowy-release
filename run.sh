#!/bin/sh

python run.py

if [ $? != 0 ]; then
  echo "Failure"
  exit 1
else
  echo "Success"
  exit 0
fi
