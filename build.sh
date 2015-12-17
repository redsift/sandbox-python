#!/bin/bash

set -eux

IMAGE="thschroeter/sandbox-python"

docker build -t ${IMAGE} .
