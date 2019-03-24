#!/bin/bash


kill -9 `ps aux |grep gunicorn |grep app | awk '{ print $2 }'`
