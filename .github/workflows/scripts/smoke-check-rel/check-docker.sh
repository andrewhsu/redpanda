#!/bin/bash
set -x -e -o pipefail
if [[ -z "$1" ]]; then
	echo error: required argument redpanda version, e.g. 22.2.1
	exit 1
fi
docker pull vectorized/redpanda:latest
REDPANDA_VERSION=$(docker run --rm --entrypoint=/usr/bin/redpanda vectorized/redpanda:latest --version)
[[ $REDPANDA_VERSION =~ ^v$1 ]]
