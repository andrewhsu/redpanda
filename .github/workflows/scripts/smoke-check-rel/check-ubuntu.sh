#!/bin/bash
set -x -e -o pipefail
if [[ -z $1 ]]; then
  echo error: required argument redpanda version
  exit 1
fi
docker pull ubuntu:latest
docker run --rm ubuntu:latest bash -c "set -e -x -o pipefail; apt update; apt-get install -y curl; curl -1sLf 'https://packages.vectorized.io/nzc4ZYQK3WRGd9sy/redpanda/cfg/setup/bash.deb.sh' | bash; apt install redpanda -y; [[ \$(dpkg-query --showformat='\${Version}' --show redpanda) =~ ^${1} ]]"
