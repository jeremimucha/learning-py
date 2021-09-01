#!/usr/bin/env bash

# Start a postgres instance

port=${1:-55432}
password=${2:-password}

exec docker run -d --rm -p ${port}:5432 --env POSTGRES_PASSWORD=${password} postgres
