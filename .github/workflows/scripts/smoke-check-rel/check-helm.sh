#!/bin/bash
set -x -e -o pipefail
if [[ -z $1 ]]; then
  echo error: required argument redpanda version, e.g. 22.2.1
  exit 1
fi
helm repo add redpanda https://charts.vectorized.io/
helm repo update
HELM_SEARCH_APP_VERSION=$(helm search repo redpanda --version "v$1" --output json | jq -r '.[].app_version')
[[ $HELM_SEARCH_APP_VERSION =~ ^v$1 ]]
