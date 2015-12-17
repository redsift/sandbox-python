#!/bin/bash

set -ux

DIR="vendor/nanomsg-python"
mkdir -p $DIR
(
	cd $DIR
	git clone https://github.com/tonysimpson/nanomsg-python .
	git reset --hard 1297015749748bd63b72a4879660884505698263
)
