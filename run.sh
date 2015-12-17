#!/bin/bash

set -eux

IMAGE="thschroeter/sandbox-python"
CONTAINER_NAME="pysbx"


docker rm -f $CONTAINER_NAME || true
docker run -d \
	-v /tmp:/run/dagger/ipc \
	--name $CONTAINER_NAME \
	$IMAGE bootstrap.py 0 1

echo 'sandbox is running'

echo 'starting test driver'
docker run -it --rm -v /tmp:/run/dagger/ipc --rm thschroeter/sandbox-python test_server.py 0 1
