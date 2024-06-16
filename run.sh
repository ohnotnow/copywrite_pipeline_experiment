#!/bin/bash
set -e

BOT_NAME=jobadreader

# Check if the container is already running
if docker ps --format '{{.Names}}' | grep -q "^${BOT_NAME}$"; then
  echo "${BOT_NAME} Container is already running"
  exit 1
fi

docker build -t ${BOT_NAME} .

docker run --restart=on-failure -v $(pwd):/data ${BOT_NAME}
