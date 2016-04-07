#!/bin/bash

set -ux

DIR="vendor/nanomsg-python"
mkdir -p $DIR
(
	cd $DIR
	git clone https://github.com/redsift/nanomsg-python .
)
