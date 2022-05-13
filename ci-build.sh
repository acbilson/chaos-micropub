#!/bin/bash

selected_rev=${1:0:7}
current_rev=$(git rev-parse --short HEAD)

if [ $selected_rev = $current_rev ]; then
   podman build --target=prod -t acbilson/micropub-$current_rev:alpine -t acbilson/micropub:latest .;
else
   echo "the current git commit and the selected commit do not match";
fi
