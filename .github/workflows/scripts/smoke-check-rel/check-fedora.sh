#!/bin/bash
set -e -o pipefail
if [[ -z $1 ]]; then
  echo error: required argument redpanda version
  exit 1
fi
docker pull fedora:latest
docker run --rm fedora:latest bash -c "set -e -x -o pipefail; curl -1sLf 'https://packages.vectorized.io/nzc4ZYQK3WRGd9sy/redpanda/cfg/setup/bash.rpm.sh' | bash; yum install redpanda -y; dnf list installed redpanda-$1"
