#!/bin/bash

set -eux

IMAGE="quay.io/redsift/sandbox-python:v2"

docker build -t ${IMAGE} .
