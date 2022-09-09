#!/bin/bash
set -x -e -o pipefail
if [[ -z $1 ]]; then
  echo error: required argument redpanda version, e.g. 22.2.1
  exit 1
fi
RELEASE_ASSETS=$(gh release view --json 'assets' --jq '.assets | length' "v$1")
(($RELEASE_ASSETS == 5))
