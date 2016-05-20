#!/bin/bash

set -eux

IMAGE="thschroeter/sandbox-python"
CONTAINER_NAME="pysbx"


docker rm -f $CONTAINER_NAME || true
docker run -u 7438 -d \
	-v /tmp:/run/sandbox/ipc \
	--name $CONTAINER_NAME \
	$IMAGE run.py 0 1

echo 'sandbox is running'

echo 'starting test driver'
docker run -u 7438 -it --rm -v /tmp:/run/sandbox/ipc --rm thschroeter/sandbox-python test_server.py 0 1
