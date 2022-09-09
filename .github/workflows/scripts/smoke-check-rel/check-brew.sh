#!/bin/bash
set -x -e -o pipefail
if [[ -z "$1" ]]; then
	echo error: required argument redpanda version, e.g. 22.2.1
	exit 1
fi
brew install redpanda-data/tap/redpanda
BREW_REDPANDA_VERSION=$(brew list --versions --formula redpanda)
[[ $BREW_REDPANDA_VERSION =~ "redpanda $1" ]]
